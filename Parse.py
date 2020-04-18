import os
from datetime import datetime

import pytz
from mdutils.mdutils import MdUtils


def hugo_build(website_src_path):
    current_path = os.getcwd()
    os.chdir(website_src_path)
    os.system(f"/snap/bin/hugo --baseURL=http://172.17.0.2")
    # os.system("docker restart nginx")
    os.chdir(current_path)
    return


def publish_status_page(containers, website_src_path):
    # Generate the about file.
    mdFile = MdUtils(
        file_name=os.path.join(website_src_path, "content", "status"),
        title="System Status",
    )

    status_table = ["Container", "Status"]
    for container in containers:
        status_table.extend(
            [
                container.attrs["Config"]["Image"].split("/")[0],
                container.attrs["State"]["Status"],
            ]
        )
    mdFile.new_line()

    mdFile.new_table(
        columns=2, rows=len(containers) + 1, text=status_table, text_align="center"
    )

    timezones = {
        "eastern": pytz.timezone("US/Eastern"),
        "amsterdam": pytz.timezone("Europe/Amsterdam"),
    }
    fmt = "%H:%M:%S (%d-%m-%Y)"

    mdFile.new_header(level=5, title="Status Update Time")

    tz_table = ["TZ", "Time"]
    for city, tz in timezones.items():
        tz_table.extend([city, datetime.now(tz).strftime(fmt)])

    mdFile.new_table(
        columns=2, rows=len(timezones) + 1, text=tz_table, text_align="center"
    )

    mdFile.create_md_file()

    # Run Hugo Build.
    hugo_build(website_src_path)

    return
