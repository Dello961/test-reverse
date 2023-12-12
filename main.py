from selenium import webdriver
from fake_useragent import UserAgent
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv


# Подмена названия браузера на случайный
ua = UserAgent()
useragent = ua.random
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent}")
options.add_argument('--incognito')
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("-–disable-popup-blocking")

# options.add_argument("--proxy-server=138.128.91.65:8000") ---> Нет актуального проплаченного proxy

service = Service(executable_path='./chromedriver.exe') 
service.start()

# Подключение Web-драйвера
driver = webdriver.Chrome(service=service, options=options)

try:
    #Включение браузера и переход на сайт
    driver.get("https://www.nseindia.com/")
    time.sleep(2)
    button = driver.find_element(By.XPATH, '//*[@id="myModal"]')
    button.send_keys(Keys.ESCAPE)
    time.sleep(2)

    # Наведение мыши на Hover элемент MARKET DATA
    hover = driver.find_element(By.XPATH, "/html/body/header/nav/div[2]/div")
    marketData = hover.find_element(By.XPATH, "/html/body/header/nav/div[2]/div/div/ul/li[3]")
    actions = ActionChains(driver).move_to_element(marketData).perform()
    time.sleep(0.6)

    # Наведение и нажатие на элемент Pre-Open Market
    pOpenM = "/html/body/header/nav/div[2]/div/div/ul/li[3]/div/div[1]/div/div[1]/ul/li[1]/a"
    preOpenMarket = marketData.find_element(By.XPATH, pOpenM)
    actions = ActionChains(driver).move_to_element(preOpenMarket).perform()
    time.sleep(0.5)
    preOpenMarket.click()
    time.sleep(2)
    html = driver.find_element(By.TAG_NAME, 'html')

    # Парсинг нужных элементов
    table = html.find_element(By.XPATH, "//table[@id='livePreTable']")
    names_price = table.find_elements(By.TAG_NAME, 'tr')

    table_info = []
    for name in names_price[1:-1]:
        info = name.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > a')
        info_price = name.find_element(By.CSS_SELECTOR, 'td.bold.text-right')
        table_info.append([info.text, info_price.text])
    
    title = ['Name', 'Price']
    with open("FinalPrice.csv", "w", newline= '') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(
                title
            )
    
    for info in table_info:
        with open("FinalPrice.csv", "a", newline= '') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(
                info
            )
    time.sleep(1)

    #Возврат на Главную страницу
    home = driver.find_element(By.XPATH, '//*[@id="link_0"]')
    actions = ActionChains(driver).move_to_element(home).perform()
    time.sleep(0.3)
    home.click()
    time.sleep(2)
    button = driver.find_element(By.XPATH, '//*[@id="myModal"]')
    button.send_keys(Keys.ESCAPE)
    time.sleep(2)

    # Переход на вкладку NIFTY BANK
    nifty_bank = driver.find_element(By.XPATH, '//*[@id="tabList_NIFTYBANK"]')
    actions = ActionChains(driver).move_to_element(nifty_bank).perform()
    time.sleep(0.6)
    nifty_bank.click()
    time.sleep(6)

    # Скрол до таблицы TOP 5 STOCKS - NIFTY 50
    html1 = driver.find_element(By.TAG_NAME, 'html')
    for i in range(13):
        html1.send_keys(Keys.DOWN)
        time.sleep(0.1)
    time.sleep(4)

    # Переход на View All
    view_all = driver.find_element(By.XPATH, '//*[@id="gainers_loosers"]/div[3]/a').get_attribute('href')
    url = view_all
    driver.get(url)
    time.sleep(4)

    # Выбор нужного  элемента в селекте NIFTY 50
    select = driver.find_element(By.CSS_SELECTOR, '#equitieStockSelect')
    actions = ActionChains(driver).move_to_element(select).click().perform()
    time.sleep(1)
    for i in range(51):
        select.send_keys(Keys.DOWN)
        time.sleep(0.1)
    alfa = select.find_element(By.CSS_SELECTOR, '#equitieStockSelect > optgroup:nth-child(4) > option:nth-child(7)')
    alfa.click()
    time.sleep(1)
    select.send_keys(Keys.ESCAPE)
    time.sleep(2)

    # Прокрутка страницы NIFTY ALPHA 50
    alfa_html = driver.find_element(By.TAG_NAME, 'html')
    time.sleep(2)
    for i in range(25):
        alfa_html.send_keys(Keys.DOWN)
        time.sleep(0.03)

    time.sleep(6)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
