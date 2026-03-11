from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random

def setup_driver():
    """Sets up the Selenium WebDriver with a custom User-Agent to mimic a real browser."""
    options = Options()
    # Add a User-Agent header
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    
    
    
    
    # Initialise Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # Set implicit wait
    driver.implicitly_wait(10)
    return driver

def scrape_baseball_data():
    driver = setup_driver()
    base_url = "https://www.baseball-almanac.com/yearmenu.shtml"
    
    print(f"Navigating to {base_url}...")
    driver.get(base_url)
    
    # lists
    events_data = []
    stats_data = []
    
    # 1. Handle pagination
    # test years
    target_years = ['2018', '2019', '2020', '2021', '2022']
    
    for year in target_years:
        print(f"\nScraping data for the year {year}...")
        try:
            # Find link for year
            year_link = driver.find_element(By.LINK_TEXT, year)
            
            # Save href 
            year_url = year_link.get_attribute('href')
            driver.get(year_url)
            
            # Wait
            time.sleep(random.uniform(2.0, 4.0))
            
            # 2. Extract Event Data: batting verage leader
            try:
                # changed 'text()' to '.' 
                event_element = driver.find_element(By.XPATH, "//td[contains(., 'Batting Average')]/following-sibling::td[1]")
                event_name = "Batting Average"
                # .strip() spaces
                event_detail = event_element.text.strip() 
            except NoSuchElementException:
                event_name = "Batting Average"
                event_detail = "Data Not Found"
                
            events_data.append({
                "Year": year,
                "Event": event_name,
                "Detail": event_detail
            })
            
            # 3. Extract Statistics Data: home run lleader
            try:
                # Changed 'text()' to '.'
                stat_element = driver.find_element(By.XPATH, "//td[contains(., 'Home Runs')]/following-sibling::td[1]")
                player_name = stat_element.text.strip()
            except NoSuchElementException:
                player_name = "Unknown"
                
            stats_data.append({
                "Year": year,
                "Statistic": "Home Runs",
                "Player": player_name
            })
            
            # Go back main menu
            driver.get(base_url)
            time.sleep(random.uniform(1.0, 2.0))
            
        except Exception as e:
            print(f"Could not process year {year}. Error: {e}")
            driver.get(base_url)
            
    driver.quit()
    
    # 4. Saveto CSVs
    print("\nSaving data to CSV files...")
    events_df = pd.DataFrame(events_data)
    stats_df = pd.DataFrame(stats_data)
    
    events_df.to_csv("events.csv", index=False)
    stats_df.to_csv("player_stats.csv", index=False)
    print("Scraping complete! Created 'events.csv' and 'player_stats.csv'.")

if __name__ == "__main__":
    scrape_baseball_data()