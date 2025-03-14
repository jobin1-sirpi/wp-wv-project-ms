import uvicorn

from .main import app


def dev_mode():
    uvicorn.run("src.main:app", use_colors=True, reload=True)


def start():
    uvicorn.run(app, host="0.0.0.0", port=5000, use_colors=True)
