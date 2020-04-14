#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from enum import Enum
import sys
import youtube_dl
import re
import requests


class Television(Enum):
    NONE = 0
    TA3 = 1
    MARKIZA = 2
    RTVS = 3
    JOJ = 4

# YTDL stuff begin


class MyLogger(object):
    """Logger class for youtube_dl Logger to tell yt-dl to print errors"""

    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)


def my_hook(d):
    """Helper function for printing, when youtube-dl has finished downloading content."""

    if d['status'] == 'finished':
        print('Done downloading')
# YTDL stuff ends


URL = "https://www.ta3.com/clanok/1180362/tb-i-matovica-po-rokovani-vlady-o-prijatych-opatreniach.html"


def get_television(webpage_url):
    match = re.match(r"https:\/\/([^\/]*)", webpage_url)
    domain = match.group(1)
    if "ta3" in domain:
        return Television.TA3
    elif "markiza" in domain:
        return Television.MARKIZA
    elif "rtvs" in domain:
        return Television.RTVS
    elif "joj" in domain:
        return Television.JOJ
    return Television.NONE


def extract_download_url(webpage):
    print('Parsing website for download url...')
    options = Options()
    options.headless = True
    television = get_television(webpage)

    if television == Television.TA3:
        with webdriver.Firefox(options=options) as driver:
            driver.get(webpage)
            player = driver.find_elements_by_class_name('fp-player')
            playlist = player[-1].find_element_by_class_name('fp-playlist')
            anchors = playlist.find_elements_by_tag_name('a')
            for anchor in anchors:
                url = anchor.get_attribute('href')
                if "livebox.cz" in url:
                    video_url = url
            heading = driver.find_element_by_class_name('heading-wrapper')
            h1 = heading.find_element_by_tag_name('h1')
            title = h1.text
            info_box = heading.find_element_by_class_name('info-box')
            m = re.match('([0-9]*).([0-9]*).([0-9]*)\ ([0-9]*)\:([0-9]*)', info_box.text)
            date = f'{m.group(3)}-{m.group(2) if len(m.group(2)) == 2 else "0" + m.group(2)}-{m.group(1) if len(m.group(1)) == 2 else "0" + m.group(1)}-{m.group(4)}-{m.group(5)}'
        print('Done')
        return f"{date} {title}", video_url
    elif television == Television.MARKIZA:
        with webdriver.Firefox(options=options) as driver:
            driver.get(webpage)
            iframe = driver.find_element_by_class_name('kframe')
            print("Markiza: Switching to iframe")
            driver.switch_to.frame(iframe)
            body = driver.find_element_by_tag_name('body')
            scripts = body.find_elements_by_tag_name('script')
            texts = [script.get_attribute('innerHTML') for script in scripts]
            for text in filter(lambda text: text, texts):
                match = re.search(r'\"hls\"\:\s\"(.*)\"', text)
                if match:
                    video_url = match.group(1)
                match = re.search(r'videoCreatedAt\:\s\"([0-9]{4})\-([0-9]{2})\-([0-9]{2})T([0-9]{2})\:([0-9]{2}).*\"',text)
                if match:
                    date = "-".join([match.group(i) for i in range(1,6)])
                match = re.search(r'videoTitle\:\s\"(.*)\"',text)
                if match:
                    title = match.group(1)
                    break

        return f"{date} {title}",video_url
    elif television == Television.RTVS:
        video_id = re.search(r'.*\/(\d*)', webpage).group(1)
        dataurl = f"https://www.rtvs.sk/json/archive5f.json?id={video_id}"
        data = requests.get(dataurl).json()["clip"]
        title = data["title"]
        date_match = re.search(r'(.*)\ (\d{2}):(\d{2})', data["datetime_create"])
        date = f'{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}'
        for source in data["sources"]:
            if "playlist.m3u8" in source["src"]:
                video_url = source["src"]
                break

        return f"{date} {title}",video_url
    elif television == Television.JOJ:
        # Joj works natively with youtube-dl, no complicated parsing of video_url required
        # Only complicated parsing of name of the video
        with webdriver.Firefox(options=options) as driver:
            driver.get(webpage)
            info = driver.find_element_by_class_name('b-video-title')
            title_el = info.find_element_by_css_selector('h2.title')
            episode_span = title_el.find_element_by_tag_name('span')
            title = title_el.text # it has name and episode withou space in it
            episode = episode_span.text
            title = title[:-len(episode)] + " " + episode
            date_el = info.find_element_by_class_name('date') # 13.04.2020
            match = re.search(r'.*\ (\d*).(\d*).(\d*)', date_el.text)
            date = f"{match.group(3)}-{match.group(2)}-{match.group(1)}"
            video_url = webpage
        return f"{date} {title}",video_url

    print("Coudn't parse")
    return "",""


def download(webpage_url):
    title, url = extract_download_url(webpage_url)

    if not title or not url:
        print("There was problem with parsing website")
        return
    ytdl_opts = {
        "format": "best",
        "progress_hooks": [my_hook],
        "outtmpl": title+".%(ext)s"
    }
    
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        ydl.download([url])


if __name__ == "__main__":
    URL = sys.argv[1]
    download(URL)
