#!/usr/bin/python3
import os
from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
# import twilio

matches_data = {}
matches_list = []


def menu():
    """Menu with user's options."""
    answer = 0
    while answer != 1 and answer != 2 and answer != 3 and answer != 4 and answer != 5:
        answer = int(input(' 1. See matchs only\n'
                           '2. Send Whatsapp message\n'
                           '3. Look for specifics TEAM\n'
                           '4. Look for Specific HOUR\n'
                           '5. Delete .txt file\n'
                           'Option: '))

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
    file_name = 'matchs' + str(f'{date.today() + timedelta(days=1)}') + '.txt'
    with open(file_name, 'w', encoding="utf-8") as file:
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
    import config  # File with numbers used and Twilio keys

    client = Client(config.account_sid, config.auth_token)

    message = client.messages.create(
        from_=config.twilio_whatsapp_number,
        body=f'{str(create_file_txt()[:1599])}',
        to=config.my_whatsapp_number
    )
    print(message.sid)
    print(create_file_txt())


def delete_txt_file():
    """Delete .txt file generated after matchs's list is shown to user."""

    file_name = 'matchs' + str(f'{date.today() + timedelta(days=1)}') + '.txt'
    if os.path.exists(file_name):
        os.remove(file_name)


def specific_team_search():
    """Search for a specific team."""

    teams = []
    file_txt = 'matchs' + str(f'{date.today() + timedelta(days=1)}') + '.txt'
    if os.path.exists(file_txt) is False:  # checks if the file was already created
        create_file_txt()

    while True:
        # Type the team name and the press Enter when don't want
        # add another team. Making the last element empty
        teams.append(input('Add team: ').capitalize())
        if teams[len(teams) - 1] == '':
            # Remove the last element.
            teams.pop()
            break

    with open(file_txt, 'r', encoding="utf-8") as file:
        for line in file:
            for team in teams:
                if team in line:
                    print(line)


def file_exists(file_name):
    """Check if the file exists"""

    # file_name = 'matchs' + str(f'{date.today() + timedelta(days=1)}') + '.txt'
    if os.path.exists(file_name) is False:
        return False

    return True


def search_by_match_hour():
    """Search for a specific hour of the day."""

    file_name = 'matchs' + str(f'{date.today() + timedelta(days=1)}') + '.txt'
    if file_exists(file_name) is False:
        create_file_txt()

    hour = input('Hour: ')
    with open(file_name, 'r', encoding="utf-8") as file:
        for line in file:
            if f'{hour}:' in line:
                print(line)


def scraper():
    """Do the scrape"""

    r = requests.get(get_url_with_date())
    soup = BeautifulSoup(r.content, 'html.parser')

    for div in soup.find(class_='Aa'):
        for matches in div.find_all('div'):
            matches_data.clear()
            if matches.find(class_='Wa') is not None:
                matches_data['league'] = matches.find(
                    'span', class_='ab').get_text(
                    )  # can't managed to get the league's name

            if matches.find(class_='ng') is not None:
                matches_data['schedule'] = matches.find(
                    'span', class_='sg og').get_text()

            if matches.find(class_='Xh') is not None:
                matches_data['home_team'] = matches.find(
                    'span', class_='Xh').get_text()

            if matches.find(class_='Zh') is not None:
                matches_data['away_team'] = matches.find(
                    'span', class_='Yh').get_text()

            if bool(matches_data):
                matches_list.append(matches_data.copy())

    return matches_list


menu()
