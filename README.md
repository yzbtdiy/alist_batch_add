## Alist 资源批量添加

**自用, Python 自学的练习项目**

**此脚测试环境为 Python 3.11, Alist v3.5.1**

* 使用 Python 基于 requests 库的发送请求
* 实现了自动获取 cookie 并保存
* 操作前验证 cookie 的有效性, cookie 无效自动更新
* 配置文件和阿里云资源文件都使用 yaml 文件便于读取数据

#### 如果您不了解Alist, 请查看官网 [https://alist.nn.ci/zh/](https://alist.nn.ci/zh/)

### 用法说明

[Bilibili视频介绍](https://www.bilibili.com/video/BV1kP4y197xm)

* 编辑 config.yaml 文件
  * 在 url 字段添加 alist 地址
  * 在 auth 后的 username 和 password 字段添加 alist 登录账号和密码
  * 在 refresh_token 字段后添加阿里云盘的 refresh_token
* 编辑 ali_share.yaml 文件
  * 添加想要的分类
  * 在分类下级添加 `资源名: 阿里云资源链接` , 链接需要需要包含 folder
* 修改完后执行 main.py 即可完成添加

### other

* alist 的登录用户和密码仅用于自动获取 cookie, 手动获取有效cookie填入config.yaml可以不用添加用户和密码
* 目前只实现了不带提取码的阿里云盘链接批量添加
