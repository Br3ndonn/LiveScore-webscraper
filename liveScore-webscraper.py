#!/usr/bin/python3
import os
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import twilio

matchs_data = {}
matchs_list = []


def menu():
    """Menu with user's options."""

    answer = int(input('1. See matchs only'
                         '\n2. Send Whatsapp message'
                         '\n3. Look for specifics TEAM'
                         '\n4. Look for Specific HOUR'
                         '\n5. Delete .txt file'
                         '\nOption: '))

    if answer == 1:
        print(create_file_txt())
        menu()
    if answer == 2:
        send_whatsapp()
        menu()
    if answer == 3:
        specific_team_search()
        menu()
    if answer == 4:
        search_by_match_hour()
        menu()
    if answer == 5:
        delete_txt_file()


def create_file_txt():
    """Create .txt file"""

    with open('matchs' + str(f'{date.today() + timedelta(days=1)}') + '.txt', 'w', encoding="utf-8") as file:
        for value in scraper():
            schedule, home_team, away_team = value.values()
            file.write(f'{schedule} {home_team} x {away_team}' + '\n')

    with open('matchs' + str(f'{date.today() + timedelta(days=1)}') + '.txt', 'r', encoding="utf-8") as file2:
        file_txt = file2.read()

    return file_txt


def get_url_with_date():
    """GET THE DESIGNATED DATE (TODAY OR TOMORROW) AND CONCATEN IT WITH THE SITE'S URL"""

    tomorrows_date = date.today() + timedelta(days=1)
    # today = "http://www.livescores.com/football/" + str(date.today()) + "/?tz=-3"
    next_day_url = "http://www.livescores.com/football/" + str(tomorrows_date) + "/?tz=-3"

    return next_day_url


def send_whatsapp():
    """Send the matchs list through whatsapp"""
    import creds  # File with numbers used and Twilio keys

    client = Client(creds.account_sid, creds.auth_token)

    message = client.messages.create(
        from_=creds.my_whatsapp_number,
        body=f'{str(create_file_txt()[:1599])}',
        to=creds.twilio_whatsapp_number
    )

    print(create_file_txt())


def delete_txt_file():
    """Delete .txt file generated after matchs's list is shown to user."""

    file_name = 'matchs' + str(f'{date.today() + timedelta(days=1)}') + '.txt'
    if os.path.exists(file_name):
        os.remove(file_name)


def specific_team_search():
    """Search for a specific team."""

    teams = []
    file_name = 'matchs' + str(f'{date.today() + timedelta(days=1)}') + '.txt'
    if os.path.exists(file_name) is False:  # checks if the file was already created
        create_file_txt()

    while True:
        teams.append(input(f'Add team: ').capitalize())
        # Press Enter when don't want add another team. Making the last element empty.
        if teams[len(teams) - 1] == '':
            # Remove the last element.
            teams.pop()
            break
    
    with open('matchs' + str(f'{date.today() + timedelta(days=1)}') + '.txt', 'r', encoding="utf-8") as file:
        for line in file:
            for team in teams:
                if team in line:
                    print(line)


def search_by_match_hour():
    """Search for a specific hour of the day."""

    file_name = 'matchs' + str(f'{date.today() + timedelta(days=1)}') + '.txt'
    if os.path.exists(file_name) is False:
        create_file_txt()

    hour = input('Hour: ')
    with open('matchs' + str(f'{date.today() + timedelta(days=1)}') + '.txt', 'r', encoding="utf-8") as file:
        for line in file:
            if f'{hour}:' in line:
                print(line)


def scraper():
    """Do the scrape"""

    r = requests.get(get_url_with_date())
    soup = BeautifulSoup(r.content, 'html.parser')

    for div in soup.find(class_='ca'):
        for matchs in div.find_all('div'):
            matchs_data.clear()
            if matchs.find(class_='yb') is not None:
                matchs_data['league'] = matchs.find('span', class_='Cb').get_text()  # cant managed to get the league's name

            if matchs.find(class_='Eg') is not None:
                matchs_data['schedule'] = matchs.find('span', class_='Jg Fg').get_text()

            if matchs.find(class_='oj') is not None:
                matchs_data['home_team'] = matchs.find('span', class_='rj').get_text()

            if matchs.find(class_='oj') is not None:
                matchs_data['away_team'] = matchs.find('span', class_='qj').get_text()
            
            if bool(matchs_data):
                matchs_list.append(matchs_data.copy())
    
    return matchs_list


menu()
