from flask import Flask, g

from proxypool.database import RedisOperator

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    """
    Connect to Redis
    """
    if not hasattr(g, 'redis_connect'):
        g.redis_connect = RedisOperator()
    return g.redis_connect


@app.route('/')
def index():
    """
    :return: HTML
    """
    return '<h1>Welcome</h1>'


@app.route('/get')
def get_proxy():
    """
    :return: HTML
    """
    conn = get_conn()
    return conn.pop()


@app.route('/count')
def get_counts():
    """
    Get the count of proxies
    """
    pool = get_conn()
    return str(pool.size)


if __name__ == '__main__':
    app.run()
