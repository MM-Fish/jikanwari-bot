import dropbox
import os


DBX_ACCESS_TOKEN = os.environ["DBX_ACCESS_TOKEN"]
dbx = dropbox.Dropbox(DBX_ACCESS_TOKEN)

values = []
for month in range(1,13):
  local_path = '%s.jpg' %month
  dbx_path = "/" + local_path

  links = dbx.sharing_list_shared_links(path=dbx_path, direct_only=True).links
  url = links[0].url
  url = url.replace('www.dropbox','dl.dropboxusercontent').replace('?dl=0','')
  values.append(url)

keys = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
pic_id = dict(zip(keys, values))
print(pic_id)