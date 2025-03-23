import time
import json
from selenium import webdriver
from bs4 import BeautifulSoup

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    return webdriver.Chrome(options=options)

def get_doctor_links(search_url, driver):
    driver.get(search_url)
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Inspect and adjust selector based on current Zocdoc layout:
    doctor_links = []
    for link in soup.find_all("a", href=True):
        if "/doctor/" in link['href']:
            full_link = "https://www.zocdoc.com" + link['href']
            doctor_links.append(full_link)
    
    doctor_links = list(set(doctor_links))  # Remove duplicates
    return doctor_links

def load_full_reviews(driver):
    # Click "Show more" button repeatedly if present
    while True:
        try:
            show_more_button = driver.find_element("class name", "sc-9l12hz-3")
            if show_more_button.is_displayed():
                driver.execute_script("arguments[0].click();", show_more_button)
                time.sleep(1)
            else:
                break
        except:
            break

def scrape_doctor_profile(driver, profile_url):
    driver.get(profile_url)
    time.sleep(2)
    load_full_reviews(driver)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    doctor_name = soup.find('h1').get_text(strip=True) if soup.find('h1') else "N/A"
    specialty_tag = soup.find('h2') or soup.find('div', class_='sc-1m56c5f-0')
    specialty = specialty_tag.get_text(strip=True) if specialty_tag else "N/A"

    reviews_data = []
    reviews = soup.find_all('div', class_='sc-1pdyj51-0')  # This class changes often, inspect Zocdoc!

    for review in reviews:
        reviewer_name = review.find('span', class_='sc-1npvkh2-1').get_text(strip=True) if review.find('span', class_='sc-1npvkh2-1') else "N/A"
        review_text = review.find('p').get_text(strip=True) if review.find('p') else "N/A"
        rating_tag = review.find('span', class_='sc-1npvkh2-3')
        rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"
        
        reviews_data.append({
            'doctor_name': doctor_name,
            'specialty': specialty,
            'profile_url': profile_url,
            'reviewer_name': reviewer_name,
            'review_text': review_text,
            'review_rating': rating
        })
    
    return reviews_data

def main():
    driver = setup_driver()
    search_url = "https://www.zocdoc.com/search?address=Alpharetta%2C%20GA&insurance_carrier=-1&day_filter=AnyDay&filters=%7B%7D&gender=-1&language=-1&offset=0&insurance_plan=-1&reason_visit=12&sees_children=false&after_5pm=false&before_10am=false&sort_type=Default&dr_specialty=98&visitType=inPersonAndVirtualVisits&search_query=Dentist&ppsSelectionId=38f749a9-1cca-471c-8ca6-ab2ce4ee00e3&searchType=specialty&searchOriginator=SearchBar&ppsSource=popular&latitude=34.12&longitude=-84.3&state=GA&city=alpharetta&locationType=placemark&searchQueryGuid="  # Example search result page
    doctor_links = get_doctor_links(search_url, driver)

    all_reviews = []

    for doctor_url in doctor_links[:5]:  # Limit for testing
        print(f"Scraping doctor: {doctor_url}")
        doctor_reviews = scrape_doctor_profile(driver, doctor_url)
        all_reviews.extend(doctor_reviews)
    
    driver.quit()

    # Save results to JSON
    with open("zocdoc_reviews.json", "w", encoding="utf-8") as f:
        json.dump(all_reviews, f, indent=4, ensure_ascii=False)

    print(f"Scraping complete! Extracted {len(all_reviews)} reviews.")

if __name__ == "__main__":
    main()
