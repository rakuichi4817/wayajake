from urllib.request import urljoin, urlopen

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def _norm_output(output):
    """ログファイルに保存する際に意図しない出力とならないように、
       正規化を行う関数

    Args:
        output (list): 複数の要素を持つ出力

    Returns:
        tuple: 正規化された出力
    """
    norm_output = list()
    stop_words = ["\t", "\n"]
    for val in output:
        for stop_word in stop_words:
            val = val.replace(stop_word, "")
        norm_output.append(val)    
    return tuple(norm_output)
    

def get_soup(url, js=False):
    """"HTMLソースをBeautifulSoupで取得

    Args:
        url (string]): 対象URL
        js (bool, optional): jsで生成されるソースを取得する場合はTrueにする. Defaults to False.

    Returns:
        bs4.BeautifulSoup: BeautifulSoupでの結果の取得
    """
    # jsの有無で処理を変える
    if js:
        # ブラウザを開かないように設定する
        options = Options()
        options.set_headless(True)
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # ブラウザを起動
        driver = webdriver.Chrome(chrome_options=options)
        # URLからHTMLを取得
        driver.get(url)
        html = driver.page_source.encode("utf-8")
        # ドライバーを閉じる
        driver.quit()
        # BeautifulSoupで扱えるようにパース
        return bs(html, "html.parser")
    else:
        return bs(urlopen(url).read().decode("utf8"), "html.parser")


# phcの最新記事情報を取得
def get_phc_latest_news():
    """pscのニュースページから最新の記事の情報を取得

    Returns:
        tupple: 最新記事をタプル（日付・タグ, タイトル, URL）で返す
    """
    # ソースの取得
    # 対象とするphcdのURL
    phc_base_url = "https://www.phchd.com/jp/"
    phc_news_url = "https://www.phchd.com/jp/news"
    soup = get_soup(phc_news_url)

    # ニューステーブルの情報を取得
    latest_news_elm =  soup.select_one("div.news_list dl div")
    
    # 1つの<dt>で囲われた日付・タグを取得し、別々の要素として扱えるように分離する
    date_tag = latest_news_elm.select_one("dt").text
    tag = latest_news_elm.select_one("dt span").text
    date = date_tag.replace(tag, "")
    # タイトルの取得
    title = latest_news_elm.select_one("dd").text
    # URLは相対リンクになっているので結合を行う。
    url = urljoin(phc_base_url, latest_news_elm.select_one("dd a").get("href"))
    
    return _norm_output([date, tag, title, url])


# JCRファーマの最新記事情報を取得
def get_jcr_latest_news():
    """JCRのニュースページから最新の記事の情報を取得

    Returns:
        tuple: 最新記事をタプル（日付, タグ, タイトル, URL）で返す
    """
    # 対象とするphcdのURL
    jcr_news_url = "https://www.jcrpharm.co.jp/news/"
    soup = get_soup(jcr_news_url, js=True)
    
    # 最新記事の一番外側になるタグでソースを取得する
    latest_news_elm = soup.select_one("#dataList > div > dl.firstChild")
    
    # 最新記事の各情報を取得する
    date = latest_news_elm.select_one("span.irDate").get_text()
    tag = latest_news_elm.select_one("span.cat-text").get_text()
    title = latest_news_elm.select_one("dd.lastChild a").get_text()
    url = latest_news_elm.select_one("a").get("href")
    
    return _norm_output([date, tag, title, url])

    
    
def get_latest_news(sitename):
    """各サイトごとの最新ニュースの情報を取得するための関数
       引数にサイト名を設定することで対応する関数を実行する

    Args:
        sitename (str): 自分で設定した関数

    Returns:
        tuple: 最新記事をタプル（日付, タグ, タイトル, URL）で返す
    """
    if sitename=="phc":
        return get_phc_latest_news()
    elif sitename=="jcr":
        return get_jcr_latest_news()
    else:
        raise ValueError("想定されていないサイト名が引数に入っています")
    
    
