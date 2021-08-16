from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# ブラウザのオプションを格納する変数をもらってきます。
options = Options()

# Headlessモードを有効にする（コメントアウトするとブラウザが実際に立ち上がります）
options.set_headless(True)

# ブラウザを起動する
driver = webdriver.Chrome(chrome_options=options)

driver.get("https://www.jcrpharm.co.jp/news/")

# HTMLを文字コードをUTF-8に変換してから取得します。
html = driver.page_source.encode("utf-8")

# ドライバーを閉じる
driver.quit()

# BeautifulSoupで扱えるようにパースします
soup = bs(html, "html.parser")

# タイトルが出力されればOK
print(soup.find("title"))

