# WayaJake

特定のHPにおける記事が更新されているか確認するスクリプト

## 準備と確認

必要とするライブラリのインストール。

```bash
pip install -r requirements.txt
```

jsを扱うためにselniumを利用するがchromedriverのインストールが必要。
このQiita記事がわかりやすい[Python + Selenium で Chrome の自動操作を一通り](https://qiita.com/memakura/items/20a02161fa7e18d8a693)

chromedriverがインストールできたらtests内のファイルを実行して動くか確認。

```bash
python tests/check_selenium.py
```

右の出力がされていたらOK。`<title>ニュース | JCRファーマ株式会社</title>`

## スクリプトの実行

```bash
python src/wayajake/main.py
```

`src/wayajake/log`内に実行記録が残る。

## 作成済みの対象サイト（2021/8/16時点）

- JCRファーマ
- PHC