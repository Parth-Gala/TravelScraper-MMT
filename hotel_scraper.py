import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pygetwindow as gw
import time

chrome_options = Options()
options = [
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
    # "--headless",
]
for option in options:
    chrome_options.add_argument(option)

chrome_service = Service('C:/Users/parth/Desktop/Travel-Website/webscraper/MakeMyTrip-scraper/chromedriver.exe')
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

initial_link = "https://www.makemytrip.com/hotels/"

driver.get(initial_link)
window_titles = gw.getAllTitles()
print("All Window Titles after link:", window_titles)

time.sleep(5)
chrome_window = gw.getWindowsWithTitle('MakeMyTrip.com: Save upto 60% on Hotel Booking 4,442,00+ Hotels Worldwide - Google Chrome')[0]
chrome_window.minimize()

user_input_city = input("Enter the city: ")

city_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'city')))
ActionChains(driver).move_to_element(city_button).click().perform()
time.sleep(2)

city_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'react-autosuggest__input')))
if city_input.is_enabled():
    driver.execute_script("arguments[0].value = '';", city_input)
    city_input.send_keys(user_input_city)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'react-autosuggest__suggestions-container')))
    time.sleep(2)
    action = ActionChains(driver)
    action.send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()


WebDriverWait(driver, 10).until(EC.invisibility_of_element_located((By.CLASS_NAME, 'hsBackDrop')))


checkin_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, 'checkin')))
ActionChains(driver).move_to_element(checkin_button).click().perform()

checkin_date = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Mon Jan 22 2024"]')))
checkin_date.click()

checkout_date = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Sat Jan 27 2024"]')))
checkout_date.click()

time.sleep(1)
apply_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//button[@data-cy="RoomsGuestsNew_327"]')))
ActionChains(driver).move_to_element(apply_button).click().perform()
time.sleep(1)

search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'hsw_search_button')))
ActionChains(driver).move_to_element(search_button).click().perform()
time.sleep(3)


WebDriverWait(driver, 10).until(EC.url_changes('current_url'))
updated_url = driver.current_url
print(f'The updated URL: {updated_url}')

# MMT_LINK = "https://www.makemytrip.com/hotels/hotel-listing/?checkin=01242024&city=CTKUU&checkout=02042024&roomStayQualifier=2e0e&locusId=CTKUU&country=IN&locusType=city&searchText=Mumbai&regionNearByExp=3&rsc=1e2e0e" 

CSV_PATH = "C:/Users/parth/Desktop/Travel-Website/webscraper/MakeMyTrip-scraper/sample_hotel_dataset.csv"

driver.get(updated_url)
time.sleep(6)
print("6 sec over")



for i in range(0,101):
    print("hotel: "+str(i))
    content = driver.find_element(By.XPATH,'//*[@id="Listing_hotel_'+str(i)+'"]')
    hname = content.find_element(By.ID,'hlistpg_hotel_name')
    print(hname.text)
    try:
        rating = content.find_element(By.ID,'hlistpg_hotel_user_rating')
        rating = rating.text
        print(rating)
        try:
            rating_desc = content.find_element(By.XPATH,'//*[@id="Listing_hotel_'+str(i)+'"]/a/div/div[1]/div[2]/div[1]/div/div/span[1]')
            rating_desc = rating_desc.text
            print(rating_desc)
        except:
            rating_desc = content.find_element(By.XPATH,'//*[@id="Listing_hotel_'+str(i)+'"]/a/div/div/div[1]/div[2]/div[2]/div/div/span[2]')
            rating_desc = rating_desc.text
            print(rating_desc.text)
        review_count = content.find_element(By.ID,'hlistpg_hotel_reviews_count')
        review_count = review_count.text
        print(review_count)
    except:
        rating=""
        rating_desc=""
        review_count=""
    
    loc = content.find_element(By.CLASS_NAME,'pc__html')
    loc = loc.text
    loc = loc.split("|")
    location = loc[0] 
    try:
        landmark = loc[1].split('from')
        dist_landmark = landmark[0].lstrip() 
        landmark = landmark[1].lstrip() 
    except:
        dist_landmark=""
        landmark=""

    print("location: "+location)
    print("landmark: "+landmark)
    print("dis to landmark: "+dist_landmark)
    
  
    price = content.find_element(By.ID,'hlistpg_hotel_shown_price')
    print(price.text[2:])
    
    tax = content.find_element(By.XPATH,'//*[@id="Listing_hotel_'+str(i)+'"]/a/div[1]/div/div[2]/div/div/p[2]')
    try:
        tax = tax.text.split(" ")[2]
    except:
        tax=""
    print(tax)
    
    try:
        s_rating = content.find_element(By.ID,'hlistpg_hotel_star_rating')
        s_rating = s_rating.get_attribute('data-content')
    except:
        s_rating=""
    
    print("s_rating: "+s_rating) 
    
    # Writing data to csv file
    data=[[hname.text,rating,rating_desc,review_count,s_rating,location,landmark,dist_landmark,price.text[2:],tax]]
    with open(CSV_PATH,'a',newline='') as file:
                writer=csv.writer(file)
                writer.writerows(data)
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

driver.close()

