from eintf.db.db import get_collection, update_collection
from eintf.extractor.news.etf import ETF
from eintf.extractor.news.rgl import RGL
from eintf.extractor.news.ugc import UGC

valid_sources = ["etf", "rgl", "ugc"]


def update_all():
    articles_etf = ETF().articles()
    articles_rgl = RGL().articles()
    articles_ugc = UGC().articles()

    date_etf = articles_etf[0].get("date") if articles_etf else -1
    date_rgl = articles_rgl[0].get("date") if articles_rgl else -1
    date_ugc = articles_ugc[0].get("date") if articles_ugc else -1

    last_update = max(
        update("etf", articles_etf, date_etf),
        update("rgl", articles_rgl, date_rgl),
        update("ugc", articles_ugc, date_ugc)
    )
    return last_update


def update(source, articles_source, date_source):
    if date_source == -1:
        return -1
    prev = get_collection("news", {"last_update": date_source})
    if prev:
        return -1
    update_collection(
        "news", {"filter": source}, {"last_update": date_source, "data": articles_source}
    )
    return date_source


def get_news(desired_sources=None):
    news = []
    if desired_sources is None:
        desired_sources = valid_sources
    desired_sources = list(filter(lambda x: x in desired_sources, valid_sources))
    for source in desired_sources:
        news += get_collection("news", {"filter": source})
    return {"success": True, "data": sorted(news, key=lambda x: x['date'], reverse=True)}