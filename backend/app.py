# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo dpkg -i google-chrome-stable_current_amd64.deb
# sudo apt-get -f install

# pip install flask flask-cors selenium webdriver-manager undetected_chromedriver

import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import undetected_chromedriver as uc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route('/api/collect-data', methods=['POST'])
def collect_data():
    logger.info("Received request to collect data")
    access_token = request.json.get('accessToken')
    if not access_token:
        logger.error("No access token provided")
        return jsonify({'status': 'error', 'message': 'No access token provided'}), 400
    
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    options.add_argument('referer=https://www.google.com/')
    options.add_argument('--start-maximized')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('detach', True) # 화면 꺼지지 않고 유지
    
    service = Service(ChromeDriverManager().install())
    driver = uc.Chrome()
    
    try:
        # 로그인 페이지로 이동
        logger.info("Navigating to Google login page")
        driver.get(f"https://accounts.google.com/v3/signin/identifier?flowEntry=ServiceLogin&flowName=GlifWebSignIn&hl=ko")
        WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.XPATH, '//span[text()="계정"]'))
        )

        logger.info("Navigating to Google activity controls page")
        driver.get("https://myactivity.google.com/myactivity?restrict=search")
        time.sleep(10)

        # 검색 기록 스크래핑
        logger.info("Scraping Google search history")
        elements = driver.find_elements(By.CSS_SELECTOR, 'div[aria-label="검색 활동 표시 카드"]')
        search_data = [element.text for element in elements if element.text.strip() != ""]
        logger.info(f"Collected {len(search_data)} search records")

        logger.info("Navigating to Google activity controls page")
        driver.get("https://myactivity.google.com/myactivity?restrict=youtube")
        time.sleep(10)

        # 유튜브 시청 기록 스크래핑
        logger.info("Scraping YouTube watch history")
        elements = driver.find_elements(By.CSS_SELECTOR, 'div[aria-label="YouTube 활동 표시 카드"]')
        youtube_data = [element.text for element in elements if element.text.strip() != ""]
        logger.info(f"Collected {len(youtube_data)} youtube records")

        
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        driver.quit()
        logger.info("WebDriver closed")

    return jsonify({'status': 'success', 'search_data': search_data, 'youtube_data': youtube_data})

if __name__ == '__main__':
    app.run(port=5000)