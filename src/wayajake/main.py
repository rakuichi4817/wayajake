import os
import webbrowser
from datetime import datetime

from scraper import get_latest_news

# ログファイルの保存用ディレクトリパス
LOGDIR = "log"
# チェックするサイトリスト
sitenames = ["phc", "jcr"]


def main():
    """メイン実行部分
    """
    # 初期化
    init_app()

    # jsなしのサイトの確認
    for sitename in sitenames:
        print(f"【{sitename}】")
        # 今までのログの取得
        log_latest_date = load_log(sitename)
        # 実行時の最新記事の取得
        site_latest_news = get_latest_news(sitename)
        if log_latest_date == site_latest_news[0]:
            # 前回取得時と同じ場合は何もしない
            print("\t更新なし")
        else:
            # 更新があった場合は
            print(f"\t更新あり\n{site_latest_news[2]}: {site_latest_news[3]}")
            # ブラウザ立ち上げ
            webbrowser.open(site_latest_news[3])
            write_log(sitename, "\t".join(site_latest_news))


def init_app():
    """初期化
    """
    # カレントディレクトリの移動
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # ディレクトリが存在していたら何もしない
    if not os.path.exists(LOGDIR):
        os.mkdir(LOGDIR)
        print(f"ログ保存ディレクトリ「{LOGDIR}」を作成しました")


def load_log(site_name):
    """特定のサイトのログテキストから最新情報を取得

    Args:
        site_name (str): 対象とするサイトの名前

    Returns:
        str or None: 最新のログを返す（ログがない場合はNoneを返す）
    """
    log_path = os.path.join(
        LOGDIR, "[{}]check_log.txt".format(site_name))  # ログファイル
    if os.path.exists(log_path):
        # ファイルが存在したときは最新のログを読み込む
        with open(log_path, "r", encoding="utf8") as fobj:
            for line in fobj:
                date = line.rstrip("\n").split("\t")[1]
                if date == "更新なし":
                    break
                latest_date = date
            return latest_date
    else:
        # ファイルがないときはログファイルの作成
        with open(log_path, "x", encoding="utf8") as fw:
            output_line = "{}\t処理スタート\n".format(datetime.now())
            fw.write(output_line)


def write_log(site_name, log_data):
    """ログファイルに書き込む

    Args:
        site_name (string): 対象となるサイト
        log_data (string):  保存する内容
    """
    log_path = os.path.join(
        LOGDIR, "[{}]check_log.txt".format(site_name))  # ログファイル
    # ファイルの一番下に書き込み
    with open(log_path, "a", encoding="utf8") as fa:
        add_line = "{}\t{}\n".format(datetime.now(), log_data)
        fa.write(add_line)


if __name__ == "__main__":
    main()
