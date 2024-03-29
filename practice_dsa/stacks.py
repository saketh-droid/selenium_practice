import json
import smtplib
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

YOUTUBE_URL = 'https://www.youtube.com/feed/trending'


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_videos(driver):
    VIDEO_DIV_TAG = 'ytd-video-renderer'
    driver.get(YOUTUBE_URL)
    videos = driver.find_elements(By.TAG_NAME, VIDEO_DIV_TAG)
    return videos


def parse_video(video):
    description = video.find_element(By.ID, 'description-text').text
    title = video.find_element(By.ID, 'video-title').text
    channel = video.find_element(By.CLASS_NAME, 'ytd-channel-name').text
    thumbnail = video.find_element(By.TAG_NAME, 'a').find_element(By.TAG_NAME, 'img').get_attribute('src')
    vid_url = video.find_element(By.ID, 'video-title').get_attribute('href')
    metadata_element = video.find_element(By.ID, 'metadata')
    metadata_line_element = metadata_element.find_element(By.ID, 'metadata-line')
    total_views = metadata_line_element.find_elements(By.TAG_NAME, 'span')[0].text
    uploaded_time = metadata_line_element.find_elements(By.TAG_NAME, 'span')[1].text
    vid_info = {
        'title': title,
        'channel': channel,
        'thumbnail': thumbnail,
        'vid_url': vid_url,
        'description': description,
        'total_views': total_views,
        'uploaded_time': uploaded_time
    }
    return vid_info


def top10_fetch():
    print('getting driver')
    driver = get_driver()
    print('started fetching content')
    videos = get_videos(driver)
    print(f'founded {len(videos)} videos')
    print('extracting videos info...')
    videos_data = [parse_video(video) for video in videos[:10]]
    videos_df = pd.DataFrame(videos_data)
    print(videos_df)
    return videos_df.to_dict(orient='records')


def Send_Email():
    try:
        with open('SENDER_PASSWORD', 'r') as file:
            SENDER_PASSWORD = file.read()
        server_ssl = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server_ssl.ehlo()

        SENDER_EMAIL = '21kb1a3042@nbkrist.org'
        RECEIVER_EMAIL = 'sakeths788@gmail.com'
        subject = 'Test message from IntelliJ'
        body = top10_fetch()
        body = json.dumps(body, indent=2)
        print(body)

        email_text = f"""
        From: {SENDER_EMAIL}
        To: {RECEIVER_EMAIL}
        Subject: {subject}
        {body}"""

        server_ssl.login(SENDER_EMAIL, str(SENDER_PASSWORD))
        server_ssl.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_text)
        server_ssl.close()

    except Exception as z:
        print(z)
    return None


if __name__ == "__main__":
    try:
        Send_Email()
    except Exception as e:
        print(e)
