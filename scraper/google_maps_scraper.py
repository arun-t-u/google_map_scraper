from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from scraper.email_scrap import scrape_email

class GoogleMapsScraper:

    def __init__(self, search_key):
        self.search_key = search_key
        options = Options()
        options.add_argument("--headless") # comment it while developing
        self.driver = webdriver.Chrome(
            service=Service(), 
            options=options
            )
        self.items = []

    def close_driver(self):
        self.driver.quit()

    def accept_gdpr(self):
        try:
            accept_button = self.driver.find_element(By.CSS_SELECTOR, "[aria-label=\"Accept all\"]")
            accept_button.click()
        except NoSuchElementException:
            print("No GDPR requirenments")

    def search(self):
        self.driver.get("https://www.google.com/maps")
        self.accept_gdpr()

        search_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#searchboxinput"))
        )
        search_input.send_keys(self.search_key)

        search_button = self.driver.find_element(By.XPATH, "//*/button[@id='searchbox-searchbutton']")
        search_button.click()

    def scroll_feed(self):
        feed_content = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]'))
        )

        self.driver.execute_script("""
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
        
    def scrape_results(self):
        self.scroll_feed()
        print("----------Scroll Completed----------------")

        maps_items = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@role="feed"]//div[contains(@jsaction, "mouseover:pane")]'))
        )

        print(f"Total Count of items: {len(maps_items)}")

        for maps_item in maps_items:
            try:
                a_tag = WebDriverWait(maps_item, 10).until(
                    EC.element_to_be_clickable((By.TAG_NAME, "a"))
                )
                time.sleep(1)
                a_tag.click()

                business_name = maps_item.find_element(By.CSS_SELECTOR, "div.fontHeadlineSmall").text
                # print(f"Business Name: {business_name}")

                # Fetch website link if available
                try:
                    website = maps_item.find_element(By.CSS_SELECTOR, 'a[data-value="Website"][jsaction][jslog]')
                    url = website.get_attribute("href")
                except NoSuchElementException:
                    url = None

                # print(f"url: {url}")

                # check for email in website
                if url:
                    try:
                        email = scrape_email(url)
                    except Exception as e:
                        print(f"Error fetching email for {business_name}: {e}")


                # Fetch phone number
                business_full_element = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '(//div[contains(@role, "main") and contains(@jslog, "mutable:true")])[2]'))
                )

                try:
                    phone_number = business_full_element.find_element(By.XPATH, "//button[contains(@aria-label, 'Phone')]/div//div[contains(@class, 'fontBodyMedium')]").text
                except NoSuchElementException:
                    phone_number = None
                # print(f"phone_number: {phone_number}")

                self.items.append({"name": business_name, "website": url, "phone_number": phone_number, "email":email})

                # Close the detail view
                close_button = business_full_element.find_element(By.XPATH, '//button[@aria-label="Close" and @data-disable-idom="true"]')

                close_button.click()
                time.sleep(1)
                print("+++++++++++++++++++++++++++++++++++++++++++")

            except Exception as e:
                print(f"Error processing item: {e}")

            
    def run(self):
        try:
            self.search()
            print("---------Search Completed!---------")
            self.scrape_results()
        finally:
            self.close_driver()
            return self.items


def scrape_in_parallel(search_terms):
    # results = []
    # with ThreadPoolExecutor(max_workers=3) as executor:  # Adjust max_workers as needed
    #     futures = [executor.submit(GoogleMapsScraper(term).run) for term in search_terms]

    #     for future in as_completed(futures):
    #         results.extend(future.result())


    google_map_scraper = GoogleMapsScraper("Interior door in California East Vale")
    results  = google_map_scraper.run()
    print(results)

    # Save results to a DataFrame
    df = pd.DataFrame(results)
    print(df)
    # df.to_csv("google_maps_results.csv", index=False)

