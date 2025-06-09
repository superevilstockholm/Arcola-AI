# Arcola AI

Arcola AI adalah sebuah website yang dapat membantu serta memudahkan pengguna.

---

## 📦 How to Install and Run

### 1. Clone this repository

- **Backend Branch:**
    ```bash
    git clone -b backend --single-branch https://github.com/superevilstockholm/Arcola-AI
    ```

- **Frontend Branch:**
    ```bash
    git clone -b frontend --single-branch https://github.com/superevilstockholm/Arcola-AI
    ```

---

### 2. Change Directory to the Project

- **Backend:**
    ```bash
    cd Arcola-AI  # folder hasil clone backend
    ```

- **Frontend:**
    ```bash
    cd Arcola-AI  # folder hasil clone frontend
    ```

---

### 3. Install Dependencies

- **Backend (Python + FastAPI):**
    ```bash
    pip install -r requirements.txt
    # dan
    cp .env.example .env
    ```

- **Frontend (Vue + npm/yarn):**
    ```bash
    npm install
    # atau
    yarn install
    ```

---

### 4. Run Development Server

- **Backend (FastAPI + Uvicorn):**
    ```bash
    uvicorn main:app --reload --host 127.0.0.1 --port 8000
    # atau
    python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
    ```

- **Frontend:**
    ```bash
    npm run serve
    # atau
    yarn dev
    ```

---

### 5. Access Project

- 🌐 **Frontend**: `http://127.0.0.1:8080`
- 🔗 **Backend Docs**:
    - `http://127.0.0.1:8000/docs` (Swagger UI) 
    - `http://127.0.0.1:8000/redoc` (Redoc) 
