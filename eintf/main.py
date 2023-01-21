from fastapi import FastAPI
from starlette.responses import JSONResponse

from .extractor.hud import Hud
from .extractor.map import Map

app = FastAPI()


@app.exception_handler(500)
async def exception_handler(request, exc):
    return JSONResponse(content={"success": False, "error": str(exc)}, status_code=500)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/huds")
def active_huds():
    return Hud().active()


@app.get("/huds/outdated")
def outdated_huds():
    return Hud().outdated()


@app.get("/huds/outdated/{hud}")
def outdated_hud(hud):
    return Hud().outdated()["data"][hud]


@app.get("/huds/{hud}")
def active_hud(hud):
    return Hud().active()["data"][hud]


@app.get("/maps/featured")
def maps(property):
    return Map().featured_downloads()
