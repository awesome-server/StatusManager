import os
import sys
import time

import docker

from Parse import publish_status_page
from utils import load_config


class StatusManager:
    def __init__(self, config):
        self.client = docker.from_env()
        self.poll_interval = config["poll_interval"]
        self.website_src_path = config["website_src_path"]

        # Start Monitoring.
        self._monitor()

    def _monitor(self):
        prev_running_containers = set()
        try:
            while True:
                running_containers = set(self.client.containers.list())
                if running_containers != prev_running_containers:
                    self._publish_status_page(running_containers)
                    prev_running_containers = running_containers

                time.sleep(self.poll_interval)

        except KeyboardInterrupt:
            print("Exiting ...")
            sys.exit(0)

    def _publish_status_page(self, status):
        publish_status_page(status, website_src_path=self.website_src_path)

    # def _generate_container(self):
    #     return set([c.attrs["Config"]["Image"]: c.attrs["State"]["Status"]
    #         for c in self.client.containers.list()
    #     }


if __name__ == "__main__":
    StatusManager(load_config("status_mgr_config.yaml"))
