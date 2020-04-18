import os
from mdutils.mdutils import MdUtils
import pytz
from datetime import datetime


def hugo_build(website_src_path):
    current_path = os.getcwd()
    os.chdir(website_src_path)
    os.system(f"/snap/bin/hugo --baseURL=http://172.17.0.2")
    os.system("docker restart nginx")
    os.chdir(current_path)
    return


def publish_status_page(status, website_src_path):
    # Generate the about file.
    mdFile = MdUtils(
        file_name=os.path.join(website_src_path, "content",  "status"),
        title="System Status",
    )

    table = ['Container', 'Status']
    for container,container_status in status.items():
        table.extend([container.split('/')[0], container_status])
    mdFile.new_line()

    mdFile.new_table(columns=2, rows=len(status) + 1, text=table, text_align='center')

    eastern = pytz.timezone('US/Eastern')
    amsterdam = pytz.timezone('Europe/Amsterdam')
    fmt = '%H:%M:%S (%d-%m-%Y)'

    AMS_time = datetime.now(amsterdam)
    MNT_time = datetime.now(eastern)

    mdFile.new_line(f"Amsterdam : {AMS_time.strftime(fmt)}")
    mdFile.new_line(f"Montreal : {MNT_time.strftime(fmt)}")

    mdFile.create_md_file()

    # Run Hugo Build.
    hugo_build(website_src_path)

    return
