import requests
from func import read_yaml, save_token, build_data

conf = read_yaml("config.yaml")
ali_list = read_yaml("ali_share.yaml")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36",
}

verify_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36",
    "Authorization": conf["token"],
}

# some alist api
login_api = conf["url"] + "/api/auth/login"
storage_list_api = conf["url"] + "/api/admin/storage/list"
add_storage_api = conf["url"] + "/api/admin/storage/create"

if conf["token"] != None:
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
        print("token无效, 尝试重新获取...")
        res = requests.post(login_api, headers=headers, json=conf["auth"])
        token = res.json()["data"]["token"]
        conf["token"] = token
        save_token(conf)
        print("token已更新, 请重新运行此脚本")
