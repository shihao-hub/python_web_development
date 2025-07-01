from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from nicegui import ui, app

router = APIRouter(tags=["test"])


def app_api():
    # core/config.py

    # db/models.py

    # routersets

    # schemas

    # services

    # utils/helpers.py

    @app.get("/data")
    def get_data():
        return {"data": [1, 2, 3]}

    # todo: 去探索一下挂载操作，似乎 django 项目可以挂载在 fastapi 项目下？
