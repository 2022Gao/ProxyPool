import redis

from proxypool.conf import HOST, PORT, POOL_NAME
from proxypool.errors import PoolEmptyError

redis_pool = redis.ConnectionPool(host=HOST, port=PORT, max_connections=20)


class RedisOperator(object):
    """Redis Operator"""

    def __init__(self):
        """Connect to Database"""

        self._conn = redis.Redis(connection_pool=redis_pool)

    def gets(self, total=1):
        """
        :param total: The number of proxies returned
        :return: proxies, size=total
        """

        tmp = self._conn.srandmember(POOL_NAME, total)
        return [s.decode('utf-8') for s in tmp]

    def puts(self, proxies: list):
        """
        :param proxies: A list with proxy as element.
        """

        # Convert type dict to type str
        str_proxies = []
        for dict_proxy in proxies:
            str_proxies.append(str(dict_proxy))

        self._conn.sadd(POOL_NAME, *str_proxies)

    def pop(self):
        """
        :return: return a proxy and delete it from database
        """
        if self.size == 0:
            raise PoolEmptyError

        try:
            str_proxy = self._conn.spop(POOL_NAME).decode('utf-8')

            # Convert type str to dict
            dic_proxy = eval(str_proxy)

            return dic_proxy

        except Exception:
            pass

    @property
    def size(self):
        """
        :return: pool.size
        """
        return self._conn.scard(POOL_NAME)

    def _flush(self):
        """
        Emptying the database
        """
        self._conn.flushall()


if __name__ == '__main__':
    pass
