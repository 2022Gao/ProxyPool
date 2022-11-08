# Redis Host
HOST = 'localhost'

# Redis PORT
PORT = 6379

# Redis set name
POOL_NAME = 'proxies'

# This link is used to check if the proxy is available.
# TEST_API = 'https://www.google.com'
TEST_API = 'https://www.baidu.com'
# TEST_API = 'https://api.bilibili.com/x/relation/stat?vmid=1&jsonp=jsonp'
# TEST_API = 'http://ip-api.com/json/'
# TEST_API = 'http://pv.sohu.com/cityjson'
# TEST_API = 'https://www.httpbin.org/get'
# TEST_API = 'https://www.google.com'
# TEST_API = 'https://blog.csdn.net/'


# lower threshold and upper threshold
# define a reasonable range of proxy pool sizes
POOL_LOWER_THRESHOLD = 10
POOL_UPPER_THRESHOLD = 40

# valid check cycle and pool len check cycle
# define a reasonable range of time
VALID_CHECK_CYCLE = 100
POOL_LEN_CHECK_CYCLE = 10

# request headers
# https://curlconverter.com/
# Use this website to construct requests headers
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://www.google.com.hk/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 '
                  'Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}
