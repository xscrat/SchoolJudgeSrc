# -- coding:utf-8 --

import requests
import globals

r = requests.post('http://%s:%s/delete_db/' % (globals.server_ip, globals.server_port))
if r.status_code == 200:
    print('删库成功')
else:
    print('删库失败')
