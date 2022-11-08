import requests
from pyquery import PyQuery as pq

from tools import Tool
from proxypool.conf import HEADERS


def get_page(url: str):
    """:return: pyquery.pyquery.PyQuery"""

    try:
        response = requests.get(url=url, headers=HEADERS, timeout=15)
        html = pq(response.text)

    except requests.Timeout as t:
        Tool.info(t.__dict__.values())
    except requests.RequestException as re:
        Tool.info(re.__dict__.values())
    except Exception as e:
        Tool.info(e.__dict__.values())

    else:
        return html


if __name__ == '__main__':
    u = 'https://www.baidu.com'
    h = get_page(url=u)
    print(type(h))
