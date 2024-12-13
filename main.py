from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd


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

search_key = "cleaning in california"
search_input.send_keys(search_key)

search_button = driver.find_element(By.XPATH, "//*/button[@id='searchbox-searchbutton']")
search_button.click()


feed_content = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]'))
)
# driver.execute_script("arguments[0].scrollIntoView(true);", feed_content)

driver.execute_script("""
          var scrollableDiv = arguments[0];
          function scrollWithinElement(scrollableDiv) {
              return new Promise((resolve, reject) => {
                  var totalHeight = 0;
                  var distance = 1000;
                  var scrollDelay = 3000;
                  
                  var timer = setInterval(() => {
                      var scrollHeightBefore = scrollableDiv.scrollHeight;
                      scrollableDiv.scrollBy(0, distance);
                      totalHeight += distance;

                      if (totalHeight >= scrollHeightBefore) {
                          totalHeight = 0;
                          setTimeout(() => {
                              var scrollHeightAfter = scrollableDiv.scrollHeight;
                              if (scrollHeightAfter > scrollHeightBefore) {
                                  return;
                              } else {
                                  clearInterval(timer);
                                  resolve();
                              }
                          }, scrollDelay);
                      }
                  }, 200);
              });
          }
          return scrollWithinElement(scrollableDiv);
  """, feed_content)



# keepScrolling = True
# timeout = 1  # Maximum wait time in seconds (default 2 minutes)
# start_time = time.time()

# while keepScrolling:
#     feed_content.send_keys(Keys.PAGE_DOWN)
#     time.sleep(0.5)
#     feed_content.send_keys(Keys.PAGE_DOWN)
#     time.sleep(0.5)

#     try:
#         WebDriverWait(driver, 0.5).until(
#             EC.presence_of_element_located((By.XPATH, "//div[@role='feed']//div//div//p[contains(@class, 'fontBodyMedium')]"))
#         )
#         print("You've reached the end of the list.")
#         keepScrolling = False
        
#     except TimeoutException:
#         if time.time() - start_time > timeout:
#             print("Timeout reached, stopping scroll.")
#             keepScrolling = False

maps_items = WebDriverWait(driver, 30).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@role="feed"]//div[contains(@jsaction, "mouseover:pane")]'))
)

print(f"Total items in list: {len(maps_items)}")
items = []
i = 0 
for maps_item in maps_items:
    # try:
    # maps_item.click()
    # Get the business name, ignoring the error if not found
    try:
        a_tag = maps_item.find_element(By.TAG_NAME, "a")
        print(a_tag.get_attribute("outerHTML"))
        a_tag.click()

        business_name = maps_item.find_element(By.CSS_SELECTOR, "div.fontHeadlineSmall").text
        print(business_name)
        # time.sleep(3)
    except:
        business_name = None
    
    business_full_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '(//div[contains(@role, "main") and contains(@jslog, "mutable:true")])[2]'))
    )

    data = {"name": business_name}

    try:
        phone_number = business_full_element.find_element(By.XPATH, "//button[contains(@aria-label, 'Phone')]/div//div[contains(@class, 'fontBodyMedium')]")
        data.update({"phone_number": phone_number.text})
    except:
        data.update({"phone_number": None})

    items.append(data)
    if i == 10:
        break
    i+=1
    button_close = business_full_element.find_element(By.XPATH, '//button[@aria-label="Close" and @data-disable-idom="true"]')
    button_close.click()
    print("-----------------")
    # except Exception as e:
    #     print(f"An error occurred: {e}")

    
df = pd.DataFrame(items)

print(df)


driver.quit()



