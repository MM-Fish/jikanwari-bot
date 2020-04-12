import dropbox
import os
from PIL import Image

DBX_ACCESS_TOKEN = os.environ["DBX_ACCESS_TOKEN"]
dbx = dropbox.Dropbox(DBX_ACCESS_TOKEN)

#スクリプト実行ディレクトリに移動
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ファイルをDropboxにアップロード
local_path = 'jikanwari.xlsx'
dbx_path = '/' + local_path
f = open(local_path, 'rb')
dbx.files_upload(f.read(),dbx_path, mode=dropbox.files.WriteMode.overwrite)
f.close()

# 画像ディレクトリに移動
os.chdir("gazou")
for month in range(1,13): 
  local_path_png = '%s.png' %month
  local_path = '%s.jpg' %month 
  im1 = Image.open(local_path_png)
  im1.save(local_path)
  dbx_path = '/' + local_path
  # ファイルをDropboxにアップロード
  f = open(local_path, 'rb')
  dbx.files_upload(f.read(),dbx_path, mode=dropbox.files.WriteMode.overwrite)
  f.close()

  # 共有リンク作成
  setting = dropbox.sharing.SharedLinkSettings(requested_visibility=dropbox.sharing.RequestedVisibility.public)
  try:       
    link = dbx.sharing_create_shared_link_with_settings(path=dbx_path, settings=setting)
  except:
    print("既に共有されています。")
print(link)