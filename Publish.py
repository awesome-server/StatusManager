import os
from datetime import datetime

import pytz
from mdutils.mdutils import MdUtils

from utils import strf_time_diff

fmt = "%H:%M:%S (%d-%m-%Y)"
timezones = {
    "eastern": pytz.timezone("US/Eastern"),
    "amsterdam": pytz.timezone("Europe/Amsterdam"),
}


def hugo_build(website_src_path):
    current_path = os.getcwd()
    os.chdir(website_src_path)
    os.system(f"/snap/bin/hugo --baseURL=http://172.17.0.2")
    # os.system("docker restart nginx")
    os.chdir(current_path)
    return


def publish_status_page(running_containers, website_src_path):
    # Generate the about file.
    mdFile = MdUtils(
        file_name=os.path.join(website_src_path, "content", "status"),
        title="System Status",
    )

    status_table = ["Container", "Status"]
    for container in sorted(
        running_containers, key=lambda c: c.attrs["Config"]["Image"].split("/")[0]
    ):
        status_table.extend(
            [
                container.attrs["Config"]["Image"].split("/")[0],
                container.attrs["State"]["Status"],
            ]
        )
    mdFile.new_line()

    mdFile.new_table(
        columns=2,
        rows=len(running_containers) + 1,
        text=status_table,
        text_align="center",
    )

    mdFile.new_header(level=5, title="Status Update Time")

    tz_table = ["TZ", "Time"]

    for city, tz in timezones.items():
        tz_table.extend([city, datetime.now().astimezone(tz).strftime(fmt)])

    mdFile.new_table(
        columns=2, rows=len(timezones) + 1, text=tz_table, text_align="center"
    )

    mdFile.create_md_file()

    return None


def publish_event_page(logs, website_src_path):
    # Generate the about file.
    mdFile = MdUtils(
        file_name=os.path.join(website_src_path, "content", "log"),
        title="Container Event Logging",
    )

    status_table = ["Container Action", "Time (UTC)"]
    for entry in logs:
        container_status = (
            ("~~" + entry[0].attrs["Config"]["Image"].split("/")[0] + "~~")
            if entry[2] == "destroyed"
            else ("**" + entry[0].attrs["Config"]["Image"].split("/")[0] + "**")
        )
        status_table.extend(
            [container_status, strf_time_diff(datetime.now(), entry[1]) + " ago"]
        )
    mdFile.new_line()

    mdFile.new_table(
        columns=2, rows=len(logs) + 1, text=status_table, text_align="center"
    )

    mdFile.new_header(level=5, title="Status Update Time")

    tz_table = ["TZ", "Time"]
    for city, tz in timezones.items():
        tz_table.extend([city, datetime.now().astimezone(tz).strftime(fmt)])

    mdFile.new_table(
        columns=2, rows=len(timezones) + 1, text=tz_table, text_align="center"
    )

    mdFile.create_md_file()

    return None
