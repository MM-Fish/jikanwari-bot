from flask import Flask, request, abort
import os
import dropbox
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

DBX_ACCESS_TOKEN = os.environ["DBX_ACCESS_TOKEN"]
dbx = dropbox.Dropbox(DBX_ACCESS_TOKEN)

values = []
for month in range(1,13):
  file_path = '%s.jpg' %month
  dbx_path = "/" + file_path

  links = dbx.sharing_list_shared_links(path=dbx_path, direct_only=True).links
  url = links[0].url
  #urlで画像を表示させる
  url = url.replace('www.dropbox','dl.dropboxusercontent').replace('?dl=0','')
  values.append(url)

keys = ['January','February','March','April','May','June','July','August','September','October','November','December']
months = [12,11,10,9,8,7,6,5,4,3,2,1]
pic_id = dict(zip(keys, values))

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #URLと
    values = []
    for month in range(1,13):
      file_path = '%s.jpg' %month
      dbx_path = "/" + file_path

      links = dbx.sharing_list_shared_links(path=dbx_path, direct_only=True).links
      url = links[0].url
      #urlで画像を表示させる
      url = url.replace('www.dropbox','dl.dropboxusercontent').replace('?dl=0','')
      values.append(url)
    keys = ['January','February','March','April','May','June','July','August','September','October','November','December']
    months = [12,11,10,9,8,7,6,5,4,3,2,1]
    pic_id = dict(zip(keys, values))

    text = event.message.text
    for month in months:
        msg = 'J' + str(month)
        if msg in text:
            a = month - 1
            key = keys[a]
            line_bot_api.reply_message(
            event.reply_token,[
            TextSendMessage(text = 'Jikanwari for ' + key),
            TextSendMessage(text = pic_id[key])
            ])

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)