import copy
import os
import sys
import time
from datetime import datetime

import docker

from Publish import hugo_build, publish_event_page, publish_status_page
from utils import load_config


class StatusManager:
    def __init__(self, config):
        self.client = docker.from_env()
        self.poll_interval = int(config["poll_interval"])
        self.website_src_path = config["website_src_path"]
        self.prev_running_containers = set()
        self.running_containers = set()
        self.logs = []

        self.mandatory_rebuild_time_diff = (
            int(config["mandatory_rebuild_time_diff"]) * 60
        )

        # Start Monitoring.
        self._monitor()

    def _monitor(self):
        try:
            while True:
                self.running_containers = set(self.client.containers.list())

                if self.running_containers != self.prev_running_containers:
                    self._publish_status_page()
                    self._publish_event_page()
                    self._rebuild_website()

                    self.prev_running_containers = self.running_containers
                    last_updated_timestamp = datetime.now()

                time.sleep(self.poll_interval)

                time_diff = datetime.now() - last_updated_timestamp
                if time_diff.seconds > self.mandatory_rebuild_time_diff:
                    self._publish_status_page()
                    self._publish_event_page()
                    self._rebuild_website()

                    last_updated_timestamp = datetime.now()

        except KeyboardInterrupt:
            print("Exiting ...")
            sys.exit(0)

    def _publish_status_page(self):
        publish_status_page(
            self.running_containers, website_src_path=self.website_src_path
        )

    def _publish_event_page(self):
        self.logs = self._generate_logs()
        publish_event_page(
            self.logs, website_src_path=self.website_src_path,
        )

    def _rebuild_website(self):
        # Run Hugo Build.
        hugo_build(self.website_src_path)

    def _generate_logs(self):
        logs = self.logs
        started_containers = [
            (container, datetime.now(), "started")
            for container in self.running_containers - self.prev_running_containers
        ]
        destroyed_containers = [
            (container, datetime.now(), "destroyed")
            for container in self.prev_running_containers - self.running_containers
        ]
        return started_containers + destroyed_containers + logs


if __name__ == "__main__":
    StatusManager(load_config("status_mgr_config.yaml"))
