import time
from bs4 import BeautifulSoup
from selenium import webdriver
from pytube import YouTube
import threading

def open_browser(url):
    browser = webdriver.Firefox()
    browser.get(url)
    time.sleep(2)
    html = browser.page_source
    browser.close()
    return html

def extract_video_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    video_urls = []
    for link in soup.find_all('a', id='thumbnail'):
        if 'href' in link.attrs:
            video_id = link['href']
            url = f"https://www.youtube.com{video_id}"
            video_urls.append(url)
        else:
            print("No href attribute found")
    return video_urls


def download_video(url, task_name):
    try:
        yt = YouTube(url)
        print('YouTube title:', yt.title)
        stream = yt.streams.get_highest_resolution()
        output_path = task_name
        stream.download(output_path)
    except Exception as e:
        print(f"Error retrieving title for video URL: {url}")
        print(f"Error message: {str(e)}")

def download_videos(url, task_name):
    html_source = open_browser(url)
    video_urls = extract_video_urls(html_source)
        
    for url in video_urls:
        download_video(url, task_name)
     
    print(f"Completed task: {task_name}")


# Main code
if __name__ == "__main__":

    channel_name = "@khanhichi99"
    video_shorts = f"https://www.youtube.com/{channel_name}/shorts"
    videos = f"https://www.youtube.com/{channel_name}/videos"
    video_streams = f"https://www.youtube.com/{channel_name}/streams"


    download_videos(video_shorts, "Shorts")
    download_videos(videos, "videos")

    

    print("All tasks completed.")








