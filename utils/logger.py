from datetime import datetime
from typing import Literal

async def log(message: str, level: Literal["info", "error", "warning"] = "info") -> None:
    colors = {
        "info": "\033[94m",
        "error": "\033[91m",
        "warning": "\033[93m",
        "reset": "\033[0m"
    }
    print(f"{colors[level]}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}{colors['reset']}", flush=True)