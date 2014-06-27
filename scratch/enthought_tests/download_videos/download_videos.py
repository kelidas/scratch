from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

profile = webdriver.FirefoxProfile('/home/kelidas/.mozilla/firefox/tq8tct7a.default')
profile.set_preference('browser.download.folderList', 2)  # custom location
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.dir', '/media/data/video/enthought_training_on_demand')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'video/webm')
profile.set_preference('media.webm.enabled', False)

driver = webdriver.Firefox(profile)
driver.implicitly_wait(10)
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
