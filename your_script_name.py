import os
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, PushMessageRequest, TextMessage
import yfinance as yf
import pandas as pd

# 環境変数から取得
CHANNEL_ACCESS_TOKEN = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)

with ApiClient(configuration) as api_client:
    line_bot_api = MessagingApi(api_client)
    line_bot_api.push_message(
        PushMessageRequest(
            to=USER_ID,
            messages=[TextMessage(text='GitHub Actionsからの通知です')]
        )
    )
    print("送信成功！")
