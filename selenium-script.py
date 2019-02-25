
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import pymongo
import math
import time
import re

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(driver, 10)

MONGO_URL = 'localhost'
MONGO_DB = 'instagram'
MONGO_TABLE = 'video_url'

def save_to_mongo(result):
    if db[MONGO_TABLE].update({'id': result['id']},{'$set': result}, True):
        print('存储成功',result)
        return True
    return False

def browse_action():
    driver.execute_script( 'window.scrollTo(0, document.body.scrollHeight)')

def main():
    try:
        driver.get('https://www.instagram.com/lotfiwoodwalker/')
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#react-root"))
        )
        
        html = driver.page_source
        doc = pq(html)
        thread_res =  doc.find('.g47SY:first').text()
        thread_num = "".join(list(filter(lambda x: x in '1234567890', thread_res))) 
        scroll_times = math.ceil(int(thread_num)/8)
        video_urls = []

        for i in range(scroll_times):
            browse_action()
            time.sleep(1)
            html = driver.page_source
            html = html.replace('xmlns', 'another_attr')
            doc = pq(html);
            items = doc.find('.v9tJq ._bz0w').items()

            for item in items:
                item_ = pq(item)
                is_video = "true" if item_.find('.u7YqG') else "false"

                url = 'https://www.instagram.com' + item_.find('a').attr('href')
                pattern = re.compile('.*p/(.*)/.*?')
                results = re.findall(pattern,url)
                result_id = results[0]
                video_urls.append({'url': url, 'id': result_id, 'is_video': is_video})

        for item in video_urls:
            save_to_mongo(item)

    except TimeoutException:
        pass

if __name__ == '__main__':
	main()