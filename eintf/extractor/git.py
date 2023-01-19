import json

import requests

release_dict = {}
util_repos = [
    ("PazerOP", "tf2_bot_detector"),
    ("mastercomfig", "mastercomfig"),
    ("JarateKing", "CleanTF2plus"),
    ("CriticalFlaw", "TF2HUD.Editor"),
    ("Narcha","DemoMan"),
]


def latest_release(owner, repo):
    release = requests.get(f"https://api.github.com/repos/{owner}/{repo}/releases/latest").json()
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
    for r in util_repos:
        append_to_dict(r)
    return json.dumps(release_dict, indent=4)


print(all_releases())
