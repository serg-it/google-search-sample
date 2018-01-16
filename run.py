import json
import re
from urllib import request, parse

GOOGLE_API_KEY = None
GOOGLE_SEARCH_ID = '016744564796170128082:8xtui_mgxte'
from local_settings import *    # noqa


def run():
    assert GOOGLE_API_KEY, GOOGLE_SEARCH_ID
    num = 10
    google_url = 'https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_SEARCH_ID}&q={search}&start={start}&num={num}'
    file = open('results.txt', 'w')
    for page in range(0, 9):
        start = page * num + 1
        with request.urlopen(google_url.format(
            GOOGLE_API_KEY=GOOGLE_API_KEY,
            GOOGLE_SEARCH_ID=GOOGLE_SEARCH_ID,
            search=parse.quote_plus('Олимпиада Корея'),
            start=start,
            num=num,
        )) as response:
            resp_json = json.loads(response.read())
        found = 0
        for item in resp_json['items']:
            match = re.compile(r'\bкоре[^.]*\bолимпиад', flags=re.M + re.I + re.U + re.DOTALL).search(item['snippet']) or \
                    re.compile(r'\bолимпиад[^.]*\bкоре', flags=re.M + re.I + re.U + re.DOTALL).search(item['snippet'])      # noqa E127
            if match and len(match.group().replace('  ', '').split()) < 5:
                found += 1
                file.write('URL: %s\n%s\n\n' % (item['link'], item['snippet']))
        if found == 0:
            break
    file.close()

if __name__ == "__main__":
    import fire
    fire.Fire(run)
