import json
import requests
from lxml import html

# Функция на получения ip
def get_ip():
    response = requests.get("https://2ip.ru/")
    if response.status_code == 200:
        tree = html.fromstring(response.text)
        span_with_ip = tree.xpath('//div[@class="ip" and @id="d_clip_button"]/span')
        ip_address = span_with_ip[0].text
        return ip_address
    else:
        print(f'Ошибка запроса: {response.status_code}')

# Функция на получения информации о тайм зоне по ip
def get_timezone_info(ip_address, token, cookie):
    post_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'X-CSRF-Token': token,
        'Cookie': cookie
    }
    post_payload = {
        'js-geoip-demo__addresses': ip_address,
        'geoip2_daemon_url': 'https://www.maxmind.com/en/geoip2-precision-demo'
    }
    post_response = requests.post("https://www.maxmind.com/en/geoip2/demo/token", data=post_payload, headers=post_headers)
    post_response_json = post_response.json()

    if 'token' in post_response_json:
        authorization_token = post_response_json['token']
        get_header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'Authorization': 'Bearer ' + authorization_token
        }
        get_responce = requests.get(f"https://geoip.maxmind.com/geoip/v2.1/city/{ip_address}?demo=1", headers=get_header)
        return get_responce.json()
    else:
        print(f'Ошибка разбора JSON')

ip_address = get_ip()
print("Текущий IP адрес: " + ip_address)

#!!! Данные в token и cookie, нужно заносить в ручную, потому что хотел реализовать запрос данных через API-key, 
# но регистрация на сайте невозможна для России а также через VPN(При получении актуальных данных код отработает корректно)!!!

token = "6c91c8a0673388761ad3455c63faedeba785f669"
cookie = "mmapiwsid=018c5e52-970a-749e-a94c-26bedc34ed10:5c1ac35e07f1b0ade1730cfbc8953af35c31ba27; mm_session=ffbea9c235b39060bb1cbf74b32035846307c1ff--cf03516763b7a1528fce39e58d4197dbb31da6bf233250cfcbf26cfa92c8bb64"

timezone_info = get_timezone_info(ip_address, token, cookie)
if 'location' in timezone_info:
    current_timezome = timezone_info['location']['time_zone']

# Получение данный с сайта со списком тайм зон и локаций
responce = requests.get("https://gist.githubusercontent.com/salkar/19df1918ee2aed6669e2/raw/84215d4a3fcdfeaabad32e87817ae5bc1073a3b7/Timezones%2520for%2520Russian%2520regions")
timezones = responce.json()

matching_regions = []
for region in timezones:
    if region[1] == current_timezome:
        matching_regions.append(region[0])

# Запись полученного списка по запрашиваемому ip в текстовой файл
with open("output.txt", "w") as file:
    file.write(current_timezome + "\n")
    file.write("\n".join(matching_regions))

print("Содержимое файла 'output.txt':")
with open("output.txt", "r") as file:
    print(file.read())
