from proxypool.conf import POOL_LOWER_THRESHOLD, POOL_UPPER_THRESHOLD, POOL_LEN_CHECK_CYCLE, VALID_CHECK_CYCLE
from proxypool.scheduler.monitor import ProxyCountCheckProcess, ExpireCheckProcess
from tools import Tool
from proxypool.webapi import app


def cli():
    Tool.if_emptying_database()
    p1 = ProxyCountCheckProcess(POOL_LOWER_THRESHOLD, POOL_UPPER_THRESHOLD, POOL_LEN_CHECK_CYCLE)
    p2 = ExpireCheckProcess(VALID_CHECK_CYCLE)
    p1.start()
    p2.start()
    app.run()
    p1.join()
    p2.join()


if __name__ == '__main__':
    cli()