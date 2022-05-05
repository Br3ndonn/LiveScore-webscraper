from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import os

dados_partidas = {}
lista_de_partidas = []


# FUNÇÕES
def menu():
    resposta = int(input('1. Apenas Ver tabela'
                         '\n2. Enviar Whatsapp'
                         '\n3. Pesquisa time específico'
                         '\n4. Pesquisa horário'
                         '\n5. Deleta arquivo txt'))

    if resposta == 1:
        print(cria_arquivo_txt())
        menu()
    if resposta == 2:
        envia_whatsapp()
        menu()
    if resposta == 3:
        pesquisa_times_especificos()
        menu()
    if resposta == 4:
        pesquisa_horario()
        menu()
    if resposta == 5:
        deleta_arquivo_txt()


def cria_arquivo_txt():
    with open('tabela' + str(f'{date.today() + timedelta(days=1)}') + '.txt', 'w', encoding="utf-8") as arquivo:
        for valor in lista_de_partidas:
            horario, time_casa, time_fora = valor.values()
            arquivo.write(f'{horario}: {time_casa} x {time_fora}' + '\n')

    with open('tabela' + str(f'{date.today() + timedelta(days=1)}') + '.txt', 'r', encoding="utf-8") as arquivo2:
        arquivo_txt = arquivo2.read()

    return arquivo_txt


def pega_url_com_data():
    """PEGA A DATA DESEJADA(HOJE OU AMANHÃ) E CONCATENA COM A URL DO SITE"""

    tomorrows_date = date.today() + timedelta(days=1)
    # today = "http://www.livescores.com/football/" + str(date.today()) + "/?tz=-3"
    next_day_url = "http://www.livescores.com/football/" + str(tomorrows_date) + "/?tz=-3"

    return next_day_url


def envia_whatsapp():

    account_sid = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+XXXXXXXXXXXX',
        body=f'{str(cria_arquivo_txt()[:1599])}',
        to='whatsapp:+XXXXXXXXXXXX'
    )

    print(message.sid)
    print(cria_arquivo_txt())


def deleta_arquivo_txt():
    """Deleta arquivo .txt gerado após lista de jogos ser mostrada ao usuário"""

    nome_arquivo = 'tabela' + str(f'{date.today() + timedelta(days=1)}') + '.txt'
    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)


def pesquisa_times_especificos():
    times = []
    cria_arquivo_txt()

    while True:
        times.append(input(f'Adicione time: ').capitalize())
        # Teclar Enter quando não quiser adicionar mais times. Tornando o último elemento vazio.
        if times[len(times) - 1] == '':
            # Remove a último elemento.
            times.pop()
            break
    with open('tabela' + str(f'{date.today() + timedelta(days=1)}') + '.txt', 'r', encoding="utf-8") as arquivo:
        for linha in arquivo:
            for time in times:
                if time in linha:
                    print(linha)


def pesquisa_horario():
    cria_arquivo_txt()
    hora = input('Horario do jogo: ')
    with open('tabela' + str(f'{date.today() + timedelta(days=1)}') + '.txt', 'r', encoding="utf-8") as arquivo:
        for linha in arquivo:
            if f'{hora}:' in linha:
                print(linha)


r = requests.get(pega_url_com_data())
soup = BeautifulSoup(r.content, 'html.parser')

for div in soup.find(class_='J'):
    for partidas in div.find_all('div'):
        dados_partidas.clear()
        if partidas.find(class_='eb') is not None:
            dados_partidas['campeonato'] = partidas.find('span', class_='hb').get_text()

        if partidas.find(class_='Gh') is not None:
            dados_partidas['horario'] = partidas.find('span', class_='ug qg').get_text()

        if partidas.find(class_='Gh') is not None:
            dados_partidas['time_casa'] = partidas.find(class_='Nh').get_text()

        if partidas.find(class_='Gh') is not None:
            dados_partidas['time_fora'] = partidas.find(class_='Mh').get_text()
        if bool(dados_partidas):
            lista_de_partidas.append(dados_partidas.copy())

menu()
