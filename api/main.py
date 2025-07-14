import warnings
import open_browser  # 不可注释,需要初始化打开web browser
# from app.azquotes.routes import client
from fastapi.responses import FileResponse

from app import create_app


warnings.simplefilter("ignore")
app = create_app()


@app.get("/")
async def index():
    return FileResponse("../dist/index.html")

# # 在应用关闭时关闭会话
# @app.on_event("shutdown")
# async def on_shutdown():
#     await client.close_session()


#     # import uvicorn
#     # uvicorn.run(app, host="0.0.0.0", port=5055)  # test  test by lly

