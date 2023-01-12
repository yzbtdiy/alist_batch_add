import yaml
import re
import json
import sys
import requests

# 读取 yaml 文件
def read_yaml(file_name):
    with open("./" + file_name, "r", encoding="utf-8") as f:
        content = yaml.load(f.read(), Loader=yaml.FullLoader)
    return content


# 保存 token 字符串
def save_token(conf):
    with open("./config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(data=conf, stream=f)


# 生成 alist 挂载阿里云盘的 json 字符串
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


# 检查配置文件是为默认值
def check_conf(conf):
    if conf["url"] == "ALIST_URL":
        sys.exit("url 未配置, 请检查配置文件")
    if (
        conf["auth"]["username"] == "USERNAME" or conf["auth"]["password"] == "PASSWORD"
    ) and (conf["token"] == "ALIST_TOKEN" or conf["token"] == ""):
        sys.exit("token和用户密码至少要配置一项, 请检查配置文件")
    if conf["refresh_token"] == "ALI_YUNPAN_REFRESH_TOKEN":
        sys.exit("refresh_token 未配置, 请检查配置文件")


# 更新 token
def update_token(login_api, headers, conf):
    print("token无效, 尝试重新获取...")
    res_data = requests.post(login_api, headers=headers, json=conf["auth"])
    if res_data.json()["code"] == 200:
        token = res_data.json()["data"]["token"]
        conf["token"] = token
        save_token(conf)
        print("token已更新, 请重新运行此脚本")
    else:
        print(res_data.json())
        sys.exit("token 更新失败, 请检查用户密码是否正确")
