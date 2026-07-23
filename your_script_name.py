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

def main():
    ticker_list = ["1540","5803","285A"]

    hantei = ""

    for code in ticker_list:
       # 銘柄コード（東京証券取引所は .T を付けます）
        ticker = f"{code}.T"
        hantei += f"{code}\n"
        
        # データの取得（過去1年分）
        df = yf.download(ticker, period="1y")

        # 25日・75日移動平均の算出
        df['SMA25'] = df['Close'].rolling(window=25).mean()
        df['SMA75'] = df['Close'].rolling(window=75).mean()

        # 直近のデータを表示（今日と昨日の分を確認）
        # print(df[['Close', 'SMA25', 'SMA75']].tail(2))

        # 最新（今日）と一つ前（昨日）の行を取得
        today_data = df.iloc[-1]
        yesterday_data = df.iloc[-2]

        # .item() を使うことで、Seriesから数値データを取り出せます
        today_sma25 = today_data['SMA25'].item()
        today_sma75 = today_data['SMA75'].item()
        yesterday_sma25 = yesterday_data['SMA25'].item()
        yesterday_sma75 = yesterday_data['SMA75'].item()

        # これで通常の数値として扱えるため、フォーマット指定が可能です
        # print(f"今日 - 25日平均: {today_sma25:.2f}, 75日平均: {today_sma75:.2f}\n昨日 - 25日平均: {yesterday_sma25:.2f}, 75日平均: {yesterday_sma75:.2f}")
        # print(f"今日 - 25日平均: {today_sma25:.2f}, 75日平均: {today_sma75:.2f}")
        # print(f"昨日 - 25日平均: {yesterday_sma25:.2f}, 75日平均: {yesterday_sma75:.2f}")
        # 昨日までは「25日平均 <= 75日平均」だったが、今日「25日平均 > 75日平均」になった
        is_golden_cross = (yesterday_sma25 <= yesterday_sma75) and (today_sma25 > today_sma75)

        # デッドクロス判定:
        # 昨日までは「25日平均 >= 75日平均」だったが、今日「25日平均 < 75日平均」になった
        is_dead_cross = (yesterday_sma25 >= yesterday_sma75) and (today_sma25 < today_sma75)

        # 結果の出力
        if is_golden_cross:
            hantei += "判定: 【ゴールデンクロス発生！】\n"
        elif is_dead_cross:
            hantei += "判定: 【デッドクロス発生！】\n"
        else:
            hantei += "判定: クロスは発生していません。\n"
        hantei += f"今日 - 25日平均: {today_sma25:.2f}, 75日平均: {today_sma75:.2f}\n昨日 - 25日平均: {yesterday_sma25:.2f}, 75日平均: {yesterday_sma75:.2f}\n\n"
    
    # 関数の呼び出し
    send_line_message(hantei)

if __name__ == "__main__":
    main()
