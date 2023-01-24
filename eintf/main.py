import time

import schedule
from fastapi import FastAPI
from starlette.responses import JSONResponse

from .extractor.hud import Hud
from .extractor.map import Map
from pymongo import MongoClient

""
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['eintf']

app = FastAPI()


@app.exception_handler(500)
async def exception_handler(request, exc):
    return JSONResponse(content={"success": False, "error": str(exc)}, status_code=500)


@app.get("/")
def read_root():
    return {}


@app.get("/huds")
def active_huds():
    return db.get_collection("huds").find_one()["active"]


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


def update_data():
    db.get_collection("huds").update_one({"active": Hud().active()}, upsert=True)


# schedule.every(30).minutes.do(update_data)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
