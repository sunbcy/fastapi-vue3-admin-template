import warnings

from app import create_app
# from app.azquotes.routes import client
from fastapi.responses import FileResponse

warnings.simplefilter("ignore")
app = create_app()


@app.get("/")
async def index():
    return FileResponse("../dist/index.html")

# # 在应用关闭时关闭会话
# @app.on_event("shutdown")
# async def on_shutdown():
#     await client.close_session()

# 启动应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5055)
