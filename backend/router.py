from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse

from aiomysql import Pool

from functools import wraps
from typing import Literal, Optional

from pydantic import ValidationError

# Models
from models.ResponseModel import BaseResponse
from models.AuthModel import RegisterModel, LoginModel, ResetPasswordByPasswordModel
from models.ProfileModel import ChangeUsernameModel, ChangeEmailModel
from models.DataUsersModel import CreateDataUsersModel, EditDataUsersModel

# Controllers
from controllers.AuthController import AuthController
from controllers.ProfileController import ProfileController
from controllers.DataUsersController import DataUsersController

from datetime import datetime

class CustomMiddlewares:
    def __init__(self, app: FastAPI, db_pool: Pool):
        self.app = app
        self.db_pool = db_pool

    def auth_middleware(self, role: list[Literal["user", "admin"]] | Literal["user", "admin"] = "user"):
        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                token_cookie = request.cookies.get("session_token")
                if not token_cookie:
                    return self._unauthorized("Cookie not found")
                async with self.db_pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("SELECT user_id, expired_at FROM sessions WHERE token = %s LIMIT 1", (token_cookie,))
                        session = await cur.fetchone()
                        if not session:
                            return self._unauthorized("Session not found")
                        user_id, expired_at = session
                        if expired_at and datetime.now() > expired_at:
                            await cur.execute("DELETE FROM sessions WHERE token = %s", (token_cookie,))
                            return self._unauthorized("Session expired")
                        await cur.execute("SELECT user_type FROM users WHERE id = %s LIMIT 1", (user_id,))
                        user = await cur.fetchone()
                        if not user:
                            return self._unauthorized("User not found")
                        user_role = user[0]
                        allowed_roles = role if isinstance(role, list) else [role]
                        if user_role not in allowed_roles:
                            return self._forbidden("Forbidden access")
                return await func(request, *args, **kwargs)
            return wrapper
        return decorator
    
    def data_verify_middleware(self, key_data: list[str]):
        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                try:
                    json_data = await request.json()
                except Exception:
                    return JSONResponse(content={"status": False, "message": "Invalid", "detail": {"reason": "Invalid JSON body"}}, status_code=400)
                if len(key_data) < len(json_data):
                    more_keys: list[str] = [key for key in json_data if key not in key_data]
                    return JSONResponse(
                        content={
                            "status": False,
                            "message": "Too many keys",
                            "detail": {
                                "keys": more_keys
                            }
                        },
                        status_code=400
                    )
                return await func(request, *args, **kwargs)
            return wrapper
        return decorator
    
    def _unauthorized(self, reason: str):
        """
        Helper function to return a 401 Unauthorized response with the given reason.

        Args:
            reason (str): The reason for the unauthorized response.

        Returns:
            JSONResponse: A JSON response with a 401 status code, a message of "Unauthorized",
            and a detail containing the given reason.
        """
        response = JSONResponse(
            content={"status": False, "message": "Unauthorized", "detail": {"reason": reason}},
            status_code=401
        )
        response.delete_cookie(key="session_token")
        return response

    def _forbidden(self, reason: str):
        """
        Helper function to return a 403 Forbidden response with the given reason.

        Args:
            reason (str): The reason for the forbidden response.

        Returns:
            JSONResponse: A JSON response with a 403 status code, a message of "Forbidden",
            and a detail containing the given reason.
        """
        response = JSONResponse(
            content={"status": False, "message": "Forbidden", "detail": {"reason": reason}},
            status_code=403
        )
        response.delete_cookie(key="session_token")
        return response
    
    async def parse_request_data(self, request: Request, model):
        """
        Parse JSON data from a request into a Pydantic model, returning an instance of the model if successful or a JSONResponse with an error message if not.

        Args:
            request: The request object
            model: The Pydantic model to parse the JSON data into

        Returns:
            A tuple containing the parsed data or None, and a JSONResponse with an error message or None
        """

        content_type = request.headers.get("content-type", "")
        if "application/json" not in content_type:
            return None, JSONResponse(
                content={"status": False, "message": "Unsupported Media Type", "detail": {"reason": "Expected 'application/json' content type"}},
                status_code=415
            )
        try:
            json_data = await request.json()
        except Exception:
            return None, JSONResponse(
                content={"status": False, "message": "Malformed JSON body", "detail": {"reason": "Body is not a valid JSON structure"}},
                status_code=400
            )
        if not isinstance(json_data, dict) or not json_data:
            return None, JSONResponse(
                content={"status": False, "message": "Empty or invalid JSON", "detail": {"reason": "Expected JSON object with fields"}},
                status_code=400
            )
        try:
            data = model(**json_data)
            return data, None
        except Exception as e:
            if isinstance(e, ValidationError):
                return None, JSONResponse(
                    content={"status": False, "message": "Validation Error", "detail": e.errors()},
                    status_code=422
                )
            raise e

    
    def __register_resource_routes__(self, controller, path: str, tags: list[str] = ["Uncategorized"], role: list[Literal["user", "admin"]] | Literal["user", "admin"] = "admin", summary: str = "", models: dict[str, str] = {}):
        """
        index: /api/resource - GET
        store: /api/resource - POST
        show: /api/resource/{item} - GET
        update: /api/resource/{item} - PUT
        delete: /api/resource/{item} - DELETE

        Needed class methods:
        - Index
        - Store
        - Show
        - Update
        - Delete

        Verify data format:
        {
            "method_name": [
                "key1", "key2", "key3"
            ],
            "store": [
                "key1", "key2", "key3"
            ],
            "edit": [
                "key1", "key2", "key3"
            ],
        }

        Models format:
        {
            "method_name": "",
            "model_name": "",
        }
        """
        resource = path.strip() # resource | data-admin | data-users | etc

        # Models
        model_store = models.get("store", None)
        model_update = models.get("update", None)

        def generate_openapi_schema(model):
            """
            Generates an OpenAPI schema for a given Pydantic model.

            Args:
                model: A Pydantic model class instance.

            Returns:
                dict: A dictionary representing the OpenAPI schema for the model,
                    formatted to include the model's JSON schema under the 
                    "application/json" content type.
            """
            return {
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": model.schema()
                        }
                    }
                }
            }

        @self.app.get(f"/api/{resource}", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True, tags=tags, summary=f"Show all {summary} data", description=f"Showing all {summary} data with {role} role type.")
        @self.auth_middleware(role=role)
        async def index(request: Request) -> JSONResponse:
            """
            Show all {summary} data.

            This endpoint is used to retrieve all {summary} data with {role} role type.

            Args:
                request (Request): The incoming request.

            Returns:
                JSONResponse: The response with the data.
            """
            return await controller.Index(request=request)
        
        @self.app.post(f"/api/{resource}", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True, tags=tags, summary=f"Create a new {summary} data", description=f"Creating a new {summary} data with {role} role type.", openapi_extra=generate_openapi_schema(model_store) if model_store else {})
        @self.auth_middleware(role=role)
        async def store(request: Request) -> JSONResponse:
            """
            Create a new {summary} data.

            This endpoint is used to create a new {summary} data with {role} role type.

            Args:
                request (Request): The incoming request containing the data to be stored.

            Returns:
                JSONResponse: The response indicating the success or failure of the operation.
            """
            if model_store:
                data, error_response = await self.parse_request_data(request, model_store)
                if error_response:
                    return error_response
                return await controller.Store(request=request, data=data)
            return await controller.Store(request=request)
        
        @self.app.get(f"/api/{resource}/{{item}}", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True, tags=tags, summary=f"Show specific {summary} data", description=f"Showing specific {summary} data with {role} role type.")
        @self.auth_middleware(role=role)
        async def show(request: Request, item: str) -> JSONResponse:
            """
            Show specific {summary} data.

            This endpoint is used to retrieve specific {summary} data with {role} role type.

            Args:
                request (Request): The incoming request.
                item (str): The item ID.

            Returns:
                JSONResponse: The response with the data.
            """
            return await controller.Show(request=request, item=item)
        
        @self.app.put(f"/api/{resource}/{{item}}", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True, tags=tags, summary=f"Update specific {summary} data", description=f"Updating specific {summary} data with {role} role type.", openapi_extra=generate_openapi_schema(model_update) if model_update else {})
        @self.auth_middleware(role=role)
        async def update(request: Request, item: str) -> JSONResponse:
            """
            Update specific {summary} data.

            This endpoint is used to update specific {summary} data with {role} role type.

            Args:
                request (Request): The incoming request.
                item (str): The item ID.

            Returns:
                JSONResponse: The response indicating the success or failure of the operation.
            """
            if model_update:
                data, error_response = await self.parse_request_data(request, model_update)
                if error_response:
                    return error_response
                return await controller.Update(request=request, item=item, data=data)
            return await controller.Update(request=request, item=item)
        
        @self.app.delete(f"/api/{resource}/{{item}}", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True, tags=tags, summary=f"Delete specific {summary} data", description=f"Deleting specific {summary} data with {role} role type.")
        @self.auth_middleware(role=role)
        async def delete(request: Request, item: str) -> JSONResponse:
            """
            Delete specific {summary} data.

            This endpoint is used to delete specific {summary} data with {role} role type.

            Args:
                request (Request): The incoming request.
                item (str): The item ID.

            Returns:
                JSONResponse: The response indicating the success or failure of the operation.
            """
            return await controller.Delete(request=request, item=item)

class Router(CustomMiddlewares):
    def __init__(self, app: FastAPI, db_pool: Pool):
        super().__init__(app=app, db_pool=db_pool)
        self.routes()

    def routes(self):
        @self.app.route("/api/ping", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"], include_in_schema=False)
        @self.auth_middleware(role=["user", "admin"])
        async def ping(request: Request) -> JSONResponse:
            """Pinging the server"""
            if request.headers.get('content-length') and int(request.headers.get('content-length')) > 100:
                return JSONResponse(content={"status": False, "message": "Payload too large", "detail": {}}, status_code=413)
            try: json_data = await request.json()
            except Exception: json_data = None
            return JSONResponse(content={"status": True, "message": "pong", "detail": { "headers": dict(request.headers), "json_data": json_data, "query": str(request.query_params), "method": request.method}}, status_code=200)
        
        @self.app.post("/api/login", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True, tags=["Auth"])
        @self.data_verify_middleware(["username", "password"])
        async def login(request: Request, userData: LoginModel) -> JSONResponse:
            """Logging in a user"""
            return await AuthController().Login(userData, self.db_pool)
        
        @self.app.post("/api/register", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True, tags=["Auth"])
        @self.data_verify_middleware(["username", "password", "email"])
        async def register(request: Request, userData: RegisterModel) -> JSONResponse:
            """Registering a new user"""
            return await AuthController().Register(userData, self.db_pool)
        
        @self.app.delete("/api/logout", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True, tags=["Auth"])
        @self.auth_middleware(role=["user", "admin"])
        async def logout(request: Request) -> JSONResponse:
            """Logging out a user"""
            return await AuthController().Logout(token=request.cookies.get("session_token"), db_pool=self.db_pool)
        
        @self.app.put("/api/user/change-password", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True, tags=["Auth"])
        @self.auth_middleware(role=["user", "admin"])
        @self.data_verify_middleware(["old_password", "new_password"])
        async def reset_password_using_password(request: Request, userData: ResetPasswordByPasswordModel) -> JSONResponse:
            """Reset password using old password"""
            return await AuthController().ResetPasswordUsingPassword(userData=userData, token=request.cookies.get("session_token"), db_pool=self.db_pool)
        
        @self.app.put("/api/user/change-username", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True, tags=["Profile"])
        @self.auth_middleware(role=["user", "admin"])
        @self.data_verify_middleware(["username"])
        async def change_username(request: Request, userData: ChangeUsernameModel) -> JSONResponse:
            """Change username"""
            return await ProfileController().ChangeUsername(userData=userData, token=request.cookies.get("session_token"), db_pool=self.db_pool)
        
        @self.app.put("/api/user/change-email", response_class=JSONResponse, response_model=BaseResponse, include_in_schema=True, tags=["Profile"])
        @self.auth_middleware(role=["user", "admin"])
        @self.data_verify_middleware(["email"])
        async def change_email(request: Request, userData: ChangeEmailModel) -> JSONResponse:
            """Change email"""
            return await ProfileController().ChangeEmail(userData=userData, token=request.cookies.get("session_token"), db_pool=self.db_pool)
        
        # Admin only
        self.__register_resource_routes__(
            path="data-users",
            controller=DataUsersController(db_pool=self.db_pool),
            role="admin",
            tags=["Admin"],
            summary="User",
            models={"store": CreateDataUsersModel, "update": EditDataUsersModel}
        )