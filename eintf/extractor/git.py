import json

import requests

release_dict = {}
util_repos = [
    ("PazerOP", "tf2_bot_detector"),
    ("mastercomfig", "mastercomfig"),
    ("JarateKing", "CleanTF2plus"),
    ("CriticalFlaw", "TF2HUD.Editor"),
    ("Narcha", "DemoMan"),
]


def latest_release(owner, repo):
    release = requests.get(f"https://api.github.com/repos/{owner}/{repo}/releases/latest").json()
    if "message" in release and release["message"] == "Not Found":
        release = requests.get(f"https://api.github.com/repos/{owner}/{repo}/commits/master").json()
        return repo, {
            "name": release["commit"]["message"],
            "published_at": release["commit"]["committer"]["date"],
            "assets": list(f"https://github.com/{owner}/{repo}/archive/refs/heads/master.zip"),
            "body": "",
            "owner": release["author"]["login"],
            "source": f"https://github.com/{owner}/{repo}",
        }
    return repo, {
        "name": release["name"],
        "published_at": release["published_at"],
        "assets": list(map(minify_asset, release["assets"])),
        "body": release["body"],
        "owner": owner,
        "source": f"https://github.com/{owner}/{repo}",
    }


def minify_asset(asset: dict):
    return {
        "url": asset["url"],
        "name": asset["name"],
        "browser_download_url": asset["browser_download_url"],
    }


def append_to_dict(repo):
    release = latest_release(repo[0], repo[1])
    release_dict[release[0]] = release[1]


def all_releases():
    try:
        for r in util_repos:
            append_to_dict(r)
        return {"success": True, "data": release_dict}
    except Exception as e:
        return {"success": False, "data": str(e)}
