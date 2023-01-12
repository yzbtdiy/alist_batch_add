import requests
from func import read_yaml, check_conf, build_data, update_token

# 读取配置文件
conf = read_yaml("config.yaml")
# 读取保存阿里云盘分享链接文件
ali_list = read_yaml("ali_share.yaml")

# 无 token 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36",
}

# 携带 token 请求头
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

# 检测 token 是否存在
if conf["token"] != "ALIST_TOKEN" and conf["token"] != "":
    # 尝试读取 storage list, 若返回 200 则说明 token 有效
    res = requests.get(storage_list_api, headers=verify_headers)
    if res.json()["code"] == 200:
        # 遍历阿里云盘资源名和链接
        for category in ali_list.keys():
            for share_name, share_url in ali_list[category].items():
                # 根据阿里云盘资源名和链接生成添加资源的 json 字符串
                push_data = build_data(
                    "/" + category + "/" + share_name, share_url, conf
                )
                # 发送请求添加资源
                result = requests.post(
                    add_storage_api, headers=verify_headers, json=push_data
                )
                # 若返回值为 200 说明添加成功
                if result.json()["code"] == 200:
                    print(category + " " + share_name + " 添加完成")
                else:
                    print(category + " " + share_name + " 添加失败, 请检查是否重复添加")
    else:
        # 若携带 token 尝试访问 storage list 失败, 则尝试更新 token 
        update_token(login_api, headers, conf)
else:
    # 若 token 为 ALIST_TOKEN 或空字符串, 则尝试更新 token
    update_token(login_api, headers, conf)
