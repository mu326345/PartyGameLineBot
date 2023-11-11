from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)
#Channel Access Token
configuration = Configuration(access_token='RJkuIv/f5RAlwvxCk49BfsBrO6wlmdRdaLOF+4nORfXeuaHujBERYOIy1fqS6mJRG5n5xHUCcfmwSda2zzIGQgTvrxfyQz0nEeWyZAAdDDwNBlnEc6u+0fPX+xnpylPNNZ20cLPrJ2PUazKw38Vw/gdB04t89/1O/w1cDnyilFU=')
#Channel Secret
handler = WebhookHandler('c6db96275c3c55c24b705b7fda8a7fcd')

# 監聽所有來自 /callback 的 Post Request
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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


#訊息傳遞區塊 
##### 基本上程式編輯都在這個function ##### 
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        # line_bot_api.push_message('U581ffde1bc9cb258045fe4d4781b57cc', TextSendMessage(text='你可以開始了'))
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

#主程式 
if __name__ == "__main__":
    app.run()