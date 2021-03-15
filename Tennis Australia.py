from helium import *
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import TimeoutException
from datetime import datetime

import pandas as pd
import random

options = ChromeOptions()
options.add_argument('--incognito')
options.add_argument('window-size=1234,800')
options.add_argument('--headless')

with open('user-agents.txt', 'r') as user_agent_file:
    user_agents_list = [str(user_agent.strip('\n')) for user_agent in user_agent_file]

driver = start_chrome(options=options)


def parse_page(postcode, page_number):
    url = f'https://www.tennis.com.au/?s={postcode}&type=coaches&proximity=30&page={page_number}'
    options.add_argument('user-agent=' + random.choice(user_agents_list))
    go_to(url)
    wait_until(S('.finder__results__container__result-main').exists)

    # Containers with relevant info

    container_tiles = driver.find_elements_by_class_name('finder__results__container__result-main__container__details')

    for tile in container_tiles:
        coach_name = tile.find_element_by_tag_name('h2').text
        location = tile.find_element_by_tag_name('h3').text
        address = tile.find_element_by_class_name('finder__results__container__result-main__container__details__address').text
        phone = str(tile.find_element_by_class_name('finder__results__container__result-main__container__details__phone').get_attribute('href').replace('tel:', ''))
        email = tile.find_element_by_class_name('finder__results__container__result-main__container__details__email').get_attribute('href').replace('mailto:', '')

        coach = {
            'Name': coach_name,
            'Location': location,
            'Address': address,
            'Phone Number': phone,
            'Email': email

        }

        print(coach)

        coaches_list.append(coach)


start_time = datetime.now()

postcode = input('Enter Postcode/Suburb/City Name: ')

coaches_list = []

try:
    i = 1
    while True:
        parse_page(postcode, i)
        i += 1
except TimeoutException:
    print('not more pages')

df = pd.DataFrame(coaches_list)
df.to_csv(f'Tennis Aus Coaches details for {postcode}.csv', index=False)

print(f'Time taken: {datetime.now() - start_time}')
