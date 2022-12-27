import json
import re
import requests

from eintf.common.helper import user_agent


class Hud:
    __active_url = "https://raw.githubusercontent.com/Hypnootize/TF2-HUDs-Megalist/master/Active%20Huds%20List.md"
    __outdated_url = "https://raw.githubusercontent.com/Hypnootize/TF2-HUDs-Megalist/master/Inactive%20Huds%20List.md"

    def active(self):
        return self.__extract(self.__active_url)

    def outdated(self):
        return self.__extract(self.__outdated_url)

    def __extract(self, url):
        response = requests.get(url, headers=user_agent())
        rows = response.text.split('\n')
        rows = filter(lambda l: "|" in l and "---" not in l, rows)
        rows = map(lambda l: l.replace('\t', ''), rows)
        rows = map(lambda l: re.sub("\\[(.*?)]", "", l), rows)
        rows = list(rows)
        #
        headers = rows.pop(0)
        headers = re.sub('[^a-zA-Z0-9|\n]', ' ', headers.replace('&', '|').lower()).split('|')
        headers = list(map(lambda t: t.replace(' ', '-'), map(lambda h: h.strip(), headers)))
        #
        return json.dumps(list(map(lambda r: self.__hud_info(r, headers), rows)), indent=4)

    def __hud_info(self, row, headers) -> (str, dict):
        columns = row.split("|")
        creator_maintainer = columns[1]
        creator = ''
        maintainer = ''
        if '`' in creator_maintainer:
            creator = re.search('`(.*)`', creator_maintainer).group(1)
        if '*' in creator_maintainer:
            maintainer = re.search('\*(.*)\*', creator_maintainer).group(1)
        columns.remove(creator_maintainer)
        columns.insert(1, creator)
        columns.insert(2, maintainer)

        columns = list(map(lambda c: c.strip("()"), columns))

        repository = columns[4].split(") (")
        columns[4] = repository

        hud_discussion = columns[7].split(") (")
        columns[7] = hud_discussion

        return {columns[0]: dict(zip(headers, columns))}
