from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import urllib
import os
import wget
import glob
import shutil

profile = webdriver.FirefoxProfile(
    '/home/kelidas/.mozilla/firefox/tq8tct7a.default')
profile.set_preference("browser.helperApps.alwaysAsk.force", False)
profile.set_preference('browser.download.folderList', 2)  # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference(
    'browser.download.dir', '/media/data/video/download')
profile.set_preference(
    'browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream,application/zip')
profile.set_preference('media.webm.enabled', False)

driver = webdriver.Firefox(profile)
#driver.set_window_size(1920 / 3, 1080)
driver.implicitly_wait(10)
driver.get("https://training.enthought.com/login")
#elem = driver.find_element_by_class_name('ng-valid-email')

# elem.send_keys(email)
# email = raw_input("Email: ")
# password = raw_input("Password: ")
# elem = driver.find_element_by_xpath("//input[@type='email']")
# elem.send_keys(email)
#
# elem = driver.find_element_by_xpath("//input[@type='password']")
# elem.send_keys(password)
# elem.send_keys(Keys.ENTER)

raw_input("waiting for click!")
driver.get('https://training.enthought.com/lectures')

time.sleep(10)
elems = driver.find_elements_by_class_name('training-entity-block')
print len(elems)
# print elems
f = open('videos.txt', 'w')
for idx in range(104, len(elems)):
    elems = driver.find_elements_by_class_name('training-entity-block')
    elem = elems[idx]
    elem.click()
    time.sleep(5)
    # print driver.page_source
    el = driver.find_elements_by_xpath('//source')
    src = el[0].get_attribute('src')
    print src
    f.write(src)

    parent = driver.find_element_by_class_name('sidebar-header')
    child = parent.find_element_by_class_name('button')
    chapter = child.get_attribute('text')
    chapter = chapter.rstrip().lstrip()
    chapter = chapter.replace(' ', '_')
    print repr(chapter)

    parent = driver.find_element_by_xpath("//li[contains(@class, 'active')]")
    parent = parent.find_element_by_class_name('toc-link')
    child = parent.find_element_by_class_name('small-10')
    name = child.get_attribute('innerHTML').replace(' ', '_')
    name = name.replace('/', '')
    print idx + 1, repr(name)

    video_pth = "/media/data/video/notes_enthought_training_on_demand/%s/%03d_%s/%s/" % (
        chapter, idx + 1, name, 'lecture')
    video_name = '%03d-%s.mp4' % (idx + 1, name)
    #urllib.urlretrieve(src, video_pth + video_name)
    #wget.download(src, video_pth + video_name)

    el = driver.find_element_by_xpath('//video')
    src_poster = el.get_attribute('poster')
    print src_poster
    jpeg_name = src_poster.split('/')[-2].lower()
    #wget.download(src_poster, video_pth + jpeg_name)

#     parent = driver.find_elements_by_class_name('lecture-notebook-link_')
#     if parent:
#         os.makedirs(video_pth)
#         for p in parent:
#             # p.click()
#             src = p.get_attribute('href')
#             fname = src.split('/')[-2].lower()
#             wget.download(src, video_pth + fname)

    video_pth = "/media/data/video/exvid_enthought_training_on_demand/%s/%03d_%s/%s/" % (
        chapter, idx + 1, name, 'examples')

#     parent = driver.find_elements_by_class_name('exercise-title')
#     if parent:
#         os.makedirs(video_pth)
#         for p in parent:
#             child = p.find_element_by_class_name('direct-exercise-link')
#             child = child.find_element_by_tag_name('a')
#             # child.click()
#             src = child.get_attribute('href')
#             fname = src.split('/')[-2].lower()
#             wget.download(src, video_pth + fname)

    parent = driver.find_elements_by_xpath("//li[@class='animate']")
    for p in parent:
        el = p.find_element_by_tag_name('a')
        if el.get_attribute('class') != 'ng-hide':
            if not os.path.exists(video_pth):
                os.makedirs(video_pth)
            el.click()
            while True:
                time.sleep(5)
                if len(driver.find_elements_by_xpath("//video")) > 1:
                    break
            video = driver.find_elements_by_xpath("//video")
            for v in video:
                # print v.get_attribute('innerHTML')
                src_ex = v.find_element_by_tag_name('source')
                src_ex = src_ex.get_attribute('src')
                if src == src_ex:
                    continue
                print src_ex
                #video_name = '%03d-%s.mp4' % (idx + 1, name)
                src_ex_fig = v.get_attribute('poster')
                if src_ex_fig:
                    jpeg_name = src_ex_fig.split('/')[-2].lower()
                ext = '.mp4'
                if 'webm' in src_ex:
                    ext = '.webm'
                #if src_ex_fig:
                    #video_name = os.path.splitext(jpeg_name)[0] + ext
                    #wget.download(src_ex, video_pth + video_name)
                    #wget.download(src_ex_fig, video_pth + jpeg_name)
                #else:
                    #wget.download(src_ex, video_pth)
                wget.download(src_ex, video_pth)
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            while True:
                time.sleep(5)
                if len(driver.find_elements_by_xpath("//video")) < 2:
                    break

    # driver.get(src)
    # time.sleep(60)
    # driver.back()
    driver.get('https://training.enthought.com/lectures')
f.close()
