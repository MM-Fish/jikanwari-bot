import sys
import requests
from requests.auth import HTTPDigestAuth
import bs4
import urllib.request
import os

import jikanwari
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta

import dropbox
import os
from PIL import Image

import edit_excel

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
excel_path = os.path.dirname(os.path.abspath(__file__)) + '/Rjikanwari.xlsx'
with open(excel_path, mode="wb") as f:
   f.write(jikanwari_content)
   print("保存しました")

#2.Excel編集
edit_excel.edit_excel('jikanwari.xlsx', '時間割', 30)

#3.時間割画像化
#3-1.画像化インスタンス作成
school_year = 2019
first_row = 4
w_nrow = 15
first_col = 'A'
last_col = 'AA'
make = jikanwari.make_gazou(school_year, first_row, w_nrow, first_col, last_col)
print(make._excel_col_ref) #Excelファイルセル番号と，日付の対応表(確認用)

#3-2.実行(毎月の時間割作成)
sheet_name = '時間割'
for i in range(0,12):
  dt = date(2019,4,1) + relativedelta(months=i)
  excel_path = os.path.dirname(os.path.abspath(__file__)) + '/Rjikanwari.xlsx'
  png_dir = os.path.dirname(os.path.abspath(__file__)) + '/gazou'
  make.make_gazou_month(dt, excel_path, png_dir, sheet_name=sheet_name)



#4.ドロップボックスに保存
DBX_ACCESS_TOKEN = os.environ["DBX_ACCESS_TOKEN"]
dbx = dropbox.Dropbox(DBX_ACCESS_TOKEN)

#4-1.ExcelファイルをDropboxにアップロード
#スクリプト実行ディレクトリに移動
os.chdir(os.path.dirname(os.path.abspath(__file__)))
local_path = 'jikanwari.xlsx'
dbx_path = '/' + local_path
f = open(local_path, 'rb')
dbx.files_upload(f.read(),dbx_path, mode=dropbox.files.WriteMode.overwrite)
f.close()
#共有リンク作成       
setting = dropbox.sharing.SharedLinkSettings(requested_visibility=dropbox.sharing.RequestedVisibility.public)
try:       
  link = dbx.sharing_create_shared_link_with_settings(path=dbx_path, settings=setting)
except:
  print("既に共有されています。")

#4-2.画像ファイルをjpg変換して，Dropboxにアップロード
#画像ディレクトリに移動
os.chdir("gazou")
for jikanwari_month in range(1,13):
  #jpgに変換
  local_path_png = '%s.png' %jikanwari_month
  local_path = '%s.jpg' %jikanwari_month 
  im1 = Image.open(local_path_png)
  im1.save(local_path)
  #アップロード
  dbx_path = '/' + local_path
  f = open(local_path, 'rb')
  dbx.files_upload(f.read(),dbx_path, mode=dropbox.files.WriteMode.overwrite)
  f.close()
  #共有リンク作成       
  setting = dropbox.sharing.SharedLinkSettings(requested_visibility=dropbox.sharing.RequestedVisibility.public)
  try:       
    link = dbx.sharing_create_shared_link_with_settings(path=dbx_path, settings=setting)
  except:
    print("既に共有されています。")
