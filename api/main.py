from fastapi import FastAPI

from api.routers.iot_device_settings import iot_device_settings_router
from api.routers.logs import logs_router

app = FastAPI()


app.include_router(logs_router)
app.include_router(iot_device_settings_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
