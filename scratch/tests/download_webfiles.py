from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

fp = webdriver.FirefoxProfile(
    '/home/kelidas/.mozilla/firefox/tq8tct7a.default')
fp.set_preference('browser.download.folderList', 2)  # custom location
fp.set_preference('browser.download.manager.showWhenStarting', False)
fp.set_preference('browser.download.dir', '/tmp/Music')

fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "audio/mp3")
fp.set_preference("browser.download.manager.showAlertOnComplete", False)
fp.set_preference('browser.helperApps.neverAsk.openFile', 'audio/mp3')
fp.set_preference("browser.helperApps.alwaysAsk.force", False)
fp.set_preference("browser.download.manager.alertOnEXEOpen", False)
fp.set_preference("browser.download.manager.focusWhenStarting", False)
fp.set_preference("browser.download.manager.useWindow", False)
fp.set_preference("browser.download.manager.closeWhenDone", True)

driver = webdriver.Firefox(fp)
driver.implicitly_wait(60)


def get_track(url):
    driver.get(url)
    elem = driver.find_element_by_id('download_link')

    elem.click()

    time.sleep(10)
    driver.close()


def get_album(url):
    driver.get(url)
    elems = driver.find_elements_by_class_name('track-title')
    print elems
    print len(elems)
    urls = [elem.get_attribute('href') for elem in elems]

    for url in urls:
        driver.get(url)
        elem = driver.find_element_by_id('download_link')

        elem.click()

        time.sleep(10)
    driver.close()

get_album(
    'http://mp3red.me/7950381/folk-song-na-cerne-hodince-u-spejblu.html')
# get_album('http://redmp3.cc/album/2228553/life-in-letters.html')
# get_track("http://redmp3.cc/17196921/christina-perri-sea-of-lovers.htmli")

'''
email = raw_input("Email: ")
password = raw_input("Password: ")
driver.get("https://training.enthought.com/#/login")
elem = driver.find_element_by_class_name('ng-valid-email')

elem.send_keys(email)
elem = driver.find_element_by_xpath("//input[@type='password']")
elem.send_keys(password)
elem.send_keys(Keys.RETURN)


driver.get('https://training.enthought.com/#/lectures')
elems = driver.find_elements_by_class_name('training-entity-block')

for idx in range(len(elems)):
    elems = driver.find_elements_by_class_name('training-entity-block')
    elem = elems[idx]
    elem.click()
    el = driver.find_elements_by_xpath('//source')
    src = el[0].get_attribute('src')
    print src
    driver.get(src)
    time.sleep(60)
    driver.back()
'''
