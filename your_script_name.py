import os
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, PushMessageRequest, TextMessage
import yfinance as yf
import pandas as pd

def send_line_message(message_text):
    """
    LINEにメッセージを送信する関数
    """
    # 環境変数から取得
    channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
    user_id = os.environ.get('LINE_USER_ID')

    configuration = Configuration(access_token=channel_access_token)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.push_message(
            PushMessageRequest(
                to=user_id,
                messages=[TextMessage(text=message_text)]
            )
        )
        print("送信成功！")

# 関数の呼び出し
send_line_message('GitHub Actions関数の呼び出しからの通知です')
