import os
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def set_driver(hidden_chrome: bool=False):
    '''
    Chromeを自動操作するためのChromeDriverを起動してobjectを取得する
    '''
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if hidden_chrome:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(f'--user-agent={USER_AGENT}') # ブラウザの種類を特定するための文字列
    options.add_argument('log-level=3') # 不要なログを非表示にする
    options.add_argument('--ignore-certificate-errors') # 不要なログを非表示にする
    options.add_argument('--ignore-ssl-errors') # 不要なログを非表示にする
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # 不要なログを非表示にする
    options.add_argument('--incognito') # シークレットモードの設定を付与
    
    ## ChromeのWebDriverオブジェクトを作成する。
    service=Service(ChromeDriverManager().install())
    return Chrome(service=service, options=options)
  
def main():
    driver = set_driver()
    
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
    
    driver.execute_script('document.querySelector(".karte-close").click()')
    time.sleep(5)
    # ポップアップを閉じる
    driver.execute_script('document.querySelector(".karte-close").click()')
    
    # 検索窓に入力
    driver.find_element(by=By.CLASS_NAME, value="topSearch__text").send_keys("高収入")
    # 検索ボタンクリック
    driver.find_element(by=By.CLASS_NAME, value="topSearch__button").click()
    
    name_elms = driver.find_elements(by=By.CLASS_NAME, value="cassetteRecruit__name")
    copy_elms = driver.find_elements(by=By.CLASS_NAME, value="cassetteRecruit__copy")
    
    
    # 空のDataFrame作成
    df = pd.DataFrame()
    df2 = pd.DataFrame()
    
    for i, name_elm in enumerate(name_elms):
        print("---------------------")
        print(f'会社名；{name_elm.text}')
        print(f'タイトル；{copy_elms[i].text}')
        # DataFrameに対して辞書形式でデータを追加する
        df = df.append(
            {"会社名": name_elm.text, 
             "タイトル": copy_elms[i].text,
             "項目C": ""}, 
            ignore_index=True)
    
    
    
# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()