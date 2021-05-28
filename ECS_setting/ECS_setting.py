import os
import configparser
import base64
import requests
import sys
import urllib
from bs4 import BeautifulSoup

INI = ("C:/ProgramData/SinPandA/data/ecs.ini")


def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()


s = requests.Session()

print("ユーザー登録")
user = input("user:")
password = input("password:")
# ログインに使うURL
url = "https://cas.ecs.kyoto-u.ac.jp/cas/login?service=https://panda.ecs.kyoto-u.ac.jp/sakai-login-tool/container"

# ログインフォームからLTを抜き出す
r1 = s.get(url)
soup = BeautifulSoup(r1.content, 'html.parser')
for input in soup.select('form input'):
    if input['name'] == 'lt':
        lt = input['value']

# ログイン処理
params = {'_eventId': 'submit', 'execution': 'e1s1', 'lt': lt,
            'username': user, 'password': password}
params = urllib.parse.urlencode(params)
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
res = s.post(url=url, data=params, headers=headers)

if(res.url != 'https://panda.ecs.kyoto-u.ac.jp/portal'):
    raise Exception

euser = encode("pand", user)
epass = encode("pand", password)

conf = configparser.ConfigParser()
if os.path.exists(INI):
    conf.read(INI)
if not "user" in conf.sections():
    conf.add_section("user")
conf.set("user", "user", euser)
conf.set("user", "password", epass)
# ファイルに書き込む


if not os.path.exists("C:/ProgramData/SinPandA"):
    os.mkdir("C:/ProgramData/SinPandA")
    os.mkdir("C:/ProgramData/SinPandA/data")
f = open(INI, "w")
conf.write(f)
f.close()
print("ユーザー登録成功")


sys.exit()
