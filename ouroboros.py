#!/usr/bin/env python3
import sys
import Ouroboros.cli as cli
from Ouroboros.logger import set_logger
from prometheus_client import start_http_server
import docker
import schedule
import logging
from Ouroboros.main import main


if __name__ == "__main__":
    log = logging.getLogger(__name__)
    args = cli.parse(sys.argv[1:])
    start_http_server(args.metrics_port, addr=args.metrics_addr)
    api_client = docker.APIClient(base_url=args.url)
    logging.basicConfig(**set_logger(args.loglevel))
    schedule.every(args.interval).seconds.do(
        main, args=args, api_client=api_client)
    log.info(f"Ouroboros configuration: {vars(args)}")

    while True:
        schedule.run_pending()
        time.sleep(1)
