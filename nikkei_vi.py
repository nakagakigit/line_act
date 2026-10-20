import os
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, PushMessageRequest, TextMessage
import yfinance as yf

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

def ni_vi():
    # 日経平均VI（ティッカー: ^NKVI.OS）のデータを取得
    ticker = "^NKVI.OS"
    vi_data = yf.Ticker(ticker)

    # 過去1ヶ月間の日次データを取得
    df = vi_data.history(period="1mo")
    print(df)

    # 最新の終値などを確認
    latest = df.iloc[-1]
    print(f"日付: {latest.name.strftime('%Y-%m-%d')}, 終値: {latest['Close']:.2f}")
    send_line_message(f" {latest['Close']:.2f}")
    
if __name__ == "__main__":
    ni_vi()