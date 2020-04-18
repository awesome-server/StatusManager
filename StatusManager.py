import os
import docker
import sys
import time

from Parse import publish_status_page
from utils import load_config


class StatusManager:
    def __init__(self, config):
        self.client = docker.from_env()
        self.poll_interval = config["poll_interval"]
        self.website_src_path = config["website_src_path"]
        self._monitor(self._generate_status_dict)

    def _monitor(self, func, *args):
        previous_status = {}
        try:
            while True:
                current_status = self._generate_status_dict()
                if current_status != previous_status:
                    self._publish_status_page(current_status)
                    previous_status = current_status

                time.sleep(self.poll_interval)

        except KeyboardInterrupt:
            print("Exiting ...")
            sys.exit(0)

    def _publish_status_page(self, status):
        publish_status_page(status, website_src_path=self.website_src_path)

    def _generate_status_dict(self):
        return {
            c.attrs["Config"]["Image"]: c.attrs["State"]["Status"]
            for c in self.client.containers.list()
        }


if __name__ == "__main__":
    StatusManager(load_config("status_mgr_config.yaml"))
