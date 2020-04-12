import sys
import requests
from requests.auth import HTTPDigestAuth
import bs4
import urllib.request
import os

#1.時間割ファイルダウンロード
#1-1.大学WebサイトURLとダイジェスト認証のuserとpass
url = os.environ["jikanwari_url"]
username = os.environ["jikanwari_user"]
password = os.environ["jikanwari_pass"]

#1-2.ファイル場所特定
#ページのアクセスとページデータ取得
res = requests.get(url,auth=HTTPDigestAuth(username,password))
content = res.content
#htmlデータ取得
data = bs4.BeautifulSoup(content, 'html.parser')
#時間割ファイル組み込みdiv要素取得
element = data.find("div", class_= "img_margin")
#div内のa要素取得
element_a = element.find("a")
#ファイルURL取得
download_url = element_a.get("href")

#1-3.ファイルダウンロード
#パスワード作成
password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, download_url, username, password)
#ファイルにアクセス
authhandler = urllib.request.HTTPDigestAuthHandler(password_manager)
opener = urllib.request.build_opener(authhandler)
#ファイル読み込み
jikanwari_content = opener.open(download_url).read()
#ローカルディレクトリにファイルを保存 
excel_path = os.path.dirname(os.path.abspath(__file__)) + '/jikanwari.xlsx'
with open(excel_path, mode="wb") as f:
   f.write(jikanwari_content)
   print("保存しました")
