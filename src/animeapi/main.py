import os
from importlib import import_module
from fastapi import FastAPI, Request
from animeapi.routes import anime, auth
from animeapi.database import create_pool
from animeapi.template import router as template_router
from animeapi.log_middleware import LogMiddleware
from animeapi.logger import logger
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(LogMiddleware)
# 设置密钥，用于加密会话数据
app.add_middleware(SessionMiddleware, secret_key="your_secret_key")
app.include_router(auth.router)
app.include_router(anime.router)
app.include_router(template_router)

# 加载插件
plugins_dir = "plugins"
if os.path.isdir(plugins_dir):
    for plugin_name in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, plugin_name)
        if os.path.isdir(plugin_path):
            try:
                plugin_module = import_module(f"animeapi.plugins.{plugin_name}.main")
                if hasattr(plugin_module, "router"):
                    app.include_router(plugin_module.router)
                else:
                    logger.error(f"Plugin {plugin_name} does not have a router.")
            except ImportError:
                logger.error(f"Failed to import plugin {plugin_name}. Error: {ImportError.path}")
else:
    logger.info("No plugins found")


@app.on_event("startup")
async def startup():
    await create_pool()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=None, reload=False)
