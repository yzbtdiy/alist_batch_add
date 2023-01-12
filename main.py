import requests
from func import read_yaml, check_conf, build_data, update_token

conf = read_yaml("config.yaml")
ali_list = read_yaml("ali_share.yaml")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36",
}

verify_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36",
    "Authorization": conf["token"],
}

# 拼接 api
login_api = conf["url"] + "/api/auth/login"
storage_list_api = conf["url"] + "/api/admin/storage/list"
add_storage_api = conf["url"] + "/api/admin/storage/create"

# 检查配置文件是否修改
check_conf(conf)

if conf["token"] != "ALIST_TOKEN" and conf["token"] != "":
    res = requests.get(storage_list_api, headers=verify_headers)
    if res.json()["code"] == 200:
        for category in ali_list.keys():
            for share_name, share_url in ali_list[category].items():
                push_data = build_data(
                    "/" + category + "/" + share_name, share_url, conf
                )
                result = requests.post(
                    add_storage_api, headers=verify_headers, json=push_data
                )
                if result.json()["code"] == 200:
                    print(category + " " + share_name + " 添加完成")
                else:
                    print(category + " " + share_name + " 添加失败, 请检查是否重复添加")
    else:
        update_token(login_api, headers, conf)
else:
    update_token(login_api, headers, conf)
