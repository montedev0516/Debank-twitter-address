from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv
import random
from selenium.common.exceptions import StaleElementReferenceException

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://debank.com/ranking?page='
page_num = 200

# Open CSV file once at the beginning
with open('twitter.csv', 'a', newline="", encoding='utf-8-sig') as open_out:
    file_o_csv = csv.writer(open_out, delimiter=',')
    
    for page_id in range(7, page_num + 1):
        driver.get(url + str(page_id))
        driver.implicitly_wait(5)

        # Retry mechanism for handling 404 errors
        retries = 3  # Number of retries for loading the page
        while retries > 0:
            try:
                if "404" in driver.title or "Page not found" in driver.page_source:
                    print(f"404 error on page {page_id}. Retrying...")
                    retries -= 1
                    sleep(2)  # Wait before retrying
                    driver.refresh()  # Refresh the page to try loading again
                else:
                    break  # Exit loop if the page is loaded successfully

            except Exception as e:
                print(f"An error occurred: {e}")
                break

        users = driver.find_elements(By.CSS_SELECTOR, 'div.db-table-row')
        
        for user in users:
            try:
                user_id = user.find_element(By.CSS_SELECTOR, 'div.db-table-cell:nth-child(1)').text
                user_name_element = user.find_element(By.CSS_SELECTOR, 'div.db-table-cell:nth-child(2)').find_element(By.CSS_SELECTOR, 'div.db-user-content')
                user_name = user_name_element.text
                user_networth = user.find_element(By.CSS_SELECTOR, 'div.db-table-cell:nth-child(3)').text
                user_tvf = user.find_element(By.CSS_SELECTOR, 'div.db-table-cell:nth-child(4)').text.split('\n')[0]
                user_followers = user.find_element(By.CSS_SELECTOR, 'div.db-table-cell:nth-child(4)').text.split('\n')[1]

                actions = ActionChains(driver)
                actions.move_to_element(user_name_element).perform()
                sleep(0.8)

                social_links = driver.find_elements(By.TAG_NAME, 'a')
                wallet_address = driver.find_element(By.TAG_NAME, 'span').text  # Ensure this selector is valid

                link_found = False
                
                for social_link in social_links:
                    try:
                        link = social_link.get_attribute('href')
                        if link and link.startswith('https://x.com/'):
                            output = [user_id, user_name, link, user_networth, user_tvf, user_followers]
                            print(output)
                            file_o_csv.writerow(output)  # Write directly to CSV
                            link_found = True
                            break
                    
                    except StaleElementReferenceException:
                        print("StaleElementReferenceException caught while accessing social links.")
                        break  # Break out of the loop and re-fetch elements if needed
                
                if not link_found:
                    output = [user_id, user_name, None, user_networth, user_tvf, user_followers]
                    print(output)
                    file_o_csv.writerow(output)  # Write with None for the link
                
                sleep(0.2)
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                sleep(0.2)

            except StaleElementReferenceException as e:
                print(f"StaleElementReferenceException caught: {e}. Retrying to fetch user data.")
                continue  # Continue to the next iteration of the loop to re-fetch elements

        sleep(random.uniform(3, 10))

# Close the WebDriver after all pages are processed
driver.quit()