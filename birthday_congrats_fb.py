from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
from bs4 import BeautifulSoup
import re


def get_html_block(login_fb, password_fb):
    #block Chrome notifications
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    driver = webdriver.Chrome('C:/projects/diploma/chromedriver.exe', chrome_options=chrome_options)

    #enter Facebook account 
    driver.get('https://www.facebook.com/')
    login_input = driver.find_element_by_name('email')
    login_input.send_keys(login_fb)
    password_input = driver.find_element_by_name('pass')
    password_input.send_keys(password_fb, Keys.RETURN)

    #get HTML block for parsing birthday people
    events = driver.find_element_by_link_text('Мероприятия').click()
    time.sleep(5)
    birthdays_all = driver.find_element_by_link_text('Дни рождения').click()
    time.sleep(5)

    birthdays_today_card = driver.find_elements_by_class_name('_fbBirthdays__todayCard')
    birthdays_list = [] 
    for birthday_html in birthdays_today_card:
        birthday_html = birthday_html.get_attribute('innerHTML')
        birthdays_list.append(birthday_html)
    return birthdays_list

def parse_birthday_friends(html_block):
    bs = BeautifulSoup(html_block, 'html.parser')
    birthday_friends = bs.find_all(attrs={'data-hovercard': True})
    
    # making list of dictionaries with friend_id and friend_name 
    birthday_friends_list = []
    for birthday_friend in birthday_friends:
        parse_name = birthday_friend.text
        birthday_friend = str(birthday_friend)
        parse_id = re.findall('profile\.php\?id=([0-9]+)"', birthday_friend)
        birthday_friend_dict = dict(user_id = parse_id, user_name = parse_name)
        birthday_friends_list.append(birthday_friend_dict)
    return birthday_friends_list

def get_users_for_congratulation():
    login_fb = ''
    password_fb = ''

    html_block = get_html_block(login_fb, password_fb)

    return parse_birthday_friends(str(html_block))

def congratulate(telegram_index, congrat_text):
    login_fb = ''
    password_fb = ''

    html_block = get_html_block(login_fb, password_fb)
    birthday_friends_list = parse_birthday_friends(str(html_block))
    
    #searching for the neccessary text-input-field to congratulate, field's index is from t-bot
    congrats_input_fields = driver.find_elements_by_name('message')
    for congrat_input_field in congrats_input_fields:
        if congrat_input_field == congrat_input_field[telegram_index]:
            congrat_input_field.send_keys(congrat_text, Keys.RETURN)


if __name__ == "__main__":
    #congrat_text = 'Happy B-Day!!!'
    #telegram_index = 0
    #users_for_congratulation = get_users_for_congratulation()
    #print(users_for_congratulation)
    #congratulate(telegram_index, congrat_text)
