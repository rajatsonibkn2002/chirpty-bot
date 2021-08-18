import requests, platform, time, json, os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def enable_download_in_headless_chrome(driver, download_dir):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    command_result = driver.execute("send_command", params)
    return driver

print("Enter Twitter Username: ")
twitterUsername = input()
chirptyURL = "https://chirpty.com/user/" + twitterUsername

completed = False

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Referer': 'https://chirpty.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'If-None-Match': 'W/"1c-GS1DarULpnoE6h7Au2UioMMwMx0"',
    'Cache-Control': 'max-age=0',
    'TE': 'trailers',
}

start = time.time()
sendMessage = True

while not completed:
    end = time.time()
    if int(end-start)%60==0 and sendMessage:
        print("\nSearching for Slots....")
        sendMessage = False
    elif int(end-start)%60!=0:
        sendMessage = True

    response = requests.get('https://chirpty.com/api/limit', headers=headers)
    data = json.loads(response.text)

    availableSlots = int(data['slots'])

    if availableSlots>0:
        print("\nWOHOOO! Slots Available")

        chrome_options = Options()  
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--log-level=OFF")

        if platform.system()=='Windows':
            chrome_path = "./chromedriver.exe"
        elif platform.system()=='Darwin':
            chrome_path = "./chromedriver_mac"
        else:
            chrome_path = "./chromedriver"  
        driver = webdriver.Chrome(executable_path = chrome_path, options=chrome_options)
        driver = enable_download_in_headless_chrome(driver, os.getcwd())

        driver.get(chirptyURL)
        time.sleep(5)

        notFound = "//span[contains(text(), 'not found')]"

        if len(driver.find_elements_by_xpath(notFound)):
            print("\nUser Not Found, Try Again with a valid username!")
        else:
            element = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Save Image')]")))
            driver.find_element_by_xpath("//button[contains(text(), 'Save Image')]").click()
            time.sleep(5)
            print("\nYayy! Download Completed, please check project directory")
        driver.quit()

        completed = True

