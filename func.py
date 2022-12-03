import yaml
import re
import json


def read_yaml(file_name):
    with open("./" + file_name, "r", encoding="utf-8") as f:
        content = yaml.load(f.read(), Loader=yaml.FullLoader)
    return content


def save_token(conf):
    with open("./config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(data=conf, stream=f)


def build_data(mount_path, ali_url, conf):
    re_id = re.compile("https://www.aliyundrive.com/s/(.+)/folder")
    re_folder = re.compile("/folder/(.+)$")
    share_id = re_id.findall(ali_url)
    root_folder_id = re_folder.findall(ali_url)
    data = {
        "mount_path": mount_path,
        "order": 0,
        "remark": "",
        "cache_expiration": 30,
        "web_proxy": False,
        "webdav_policy": "302_redirect",
        "down_proxy_url": "",
        "extract_folder": "",
        "driver": "AliyundriveShare",
        "addition": {
            "refresh_token": conf["refresh_token"],
            "share_id": share_id[0],
            "share_pwd": "",
            "root_folder_id": root_folder_id[0],
            "order_by": "",
            "order_direction": "",
        },
    }
    data["addition"] = json.dumps(data["addition"], separators=(",", ":"))
    return data
