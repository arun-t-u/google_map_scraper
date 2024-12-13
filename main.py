from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
driver.get("https://www.google.com/maps")

# to deal with the option GDPR options
try:
     # select the "Accept all" button from the GDPR cookie option page
    accept_button = driver.find_element(By.CSS_SELECTOR, "[aria-label=\"Accept all\"]")
    # click it
    accept_button.click()
except NoSuchElementException:
    print("No GDPR requirenments")

search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "#searchboxinput"))
)

search_key = "Hotels in kerala"
search_input.send_keys(search_key)

search_button = driver.find_element(By.XPATH, "//*/button[@id='searchbox-searchbutton']")
search_button.click()


feed_content = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]'))
)
driver.execute_script("arguments[0].scrollIntoView(true);", feed_content)


keepScrolling = True
timeout = 180  # Maximum wait time in seconds (default 2 minutes)
start_time = time.time()

while keepScrolling:
    feed_content.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)
    feed_content.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.5)

    try:
        WebDriverWait(driver, 0.5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='feed']//div//div//p[contains(@class, 'fontBodyMedium')]"))
        )
        time.sleep(5)
        print("You've reached the end of the list.")
        keepScrolling = False
        
    except TimeoutException:
        if time.time() - start_time > timeout:
            print("Timeout reached, stopping scroll.")
            keepScrolling = False

maps_items = WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@role="feed"]//div[contains(@jsaction, "mouseover:pane")]'))
)

print(len(maps_items)) 
# //div[@role="feed


driver.quit()



