from fastapi import FastAPI
from starlette.responses import JSONResponse

from .common.helper import now
from .db.db import get_collection, update_collection
from .extractor.git import latest_release, all_releases
from .extractor.hud import Hud
from .extractor.news.all import get_news, update_all

# from common.helper import now
# from extractor.git import latest_release, all_releases
# from extractor.hud import Hud
# from extractor.news.all import get_news

app = FastAPI()


@app.exception_handler(500)
async def exception_handler(request, exc):
    return JSONResponse(content={"success": False, "error": str(exc)}, status_code=500)


@app.get("/")
def read_root():
    return {}


@app.get("/huds")
@app.get("/huds/active")
def active_huds():
    return get_collection("huds", key="active")


@app.get("/huds/{hud}")
def active_hud(hud):
    return get_collection("huds", key="active")["data"][hud]


@app.get("/tools")
def tools():
    return get_collection("tools")


@app.get("/tools/{tool_}")
def tool(tool_):
    return get_collection("tools", key="data")["data"][tool_]


@app.get("/news")
def news_all():
    return get_news()


@app.get("/news?sources={sources}")
def news(source):
    return get_news(source.split(","))


@app.get("/update/{it}")
def update_data(it):
    if it == "huds":
        last_update_date = latest_release("Hypnootize", "TF2-HUDs-Megalist")[1]["published_at"]
        db_update_date = get_collection("huds", {"status": "active"}, key="last_update")
        if db_update_date == last_update_date:
            return {"success": False, "message": "Already updated"}
        update_collection(
            "huds",
            {"status": "active"},
            {"status": "active", "last_update": last_update_date, "data": Hud().active()},
            True
        )
        return {"success": True, "message": last_update_date}

    elif it == "tools":
        db_update_date = get_collection("tools", {"last_update": {"$gt": now() - 86400}})
        if db_update_date:
            return {"success": False, "message": "Already updated"}
        update_collection(
            "tools",
            {"filter": "all"},
            {"last_update": now(), "data": all_releases()},
            True
        )
        return {"success": True, "message": now()}

    elif it == "news":
        updated = update_all()
        if updated == -1:
            return {"success": False, "message": "Already updated"}
        else:
            return {"success": True, "message": updated}
