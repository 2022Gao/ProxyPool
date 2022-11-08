import logging

from proxypool.database import RedisOperator

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d - %(message)s',
                    datefmt='%H:%M:%S')


class Tool:

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def if_emptying_database():
        pool = RedisOperator()
        size = pool.size
        logging.info(f'There are a total of {size} old proxies in current database.'
                     f'Do you want to clean them? (yes/no) -> ')

        s = input().lower()
        if s == 'yes':
            pool._flush()
            logging.info('\nThe database was emptied successfully')


if __name__ == '__main__':
    pass
