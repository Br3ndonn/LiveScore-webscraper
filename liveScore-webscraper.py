import datetime
from bs4 import BeautifulSoup
import requests
from twilio.rest import Client

dados = dict()
lista = list()

# PEGA A DATA DESEJADA(HOJE OU AMANHÃ) E CONCATENA COM A URL DO SITE
tomorrows_date = datetime.date.today() + datetime.timedelta(days=1)
today = "http://www.livescores.com/football/" + str(datetime.date.today()) + "/?tz=-3"
next_day_url = "http://www.livescores.com/football/" + str(tomorrows_date) + "/?tz=-3"

# REQUEST DO SITE
site = requests.get(next_day_url)
soup = BeautifulSoup(site.content, 'html.parser')

# PERCORRE O CÓDIGO HTML EM BUSCA DOS ELEMENTOS DESEJADOS

for div in soup.find(class_='MatchRows_root__1NKae'):
    for jogos in div.find_all('div'):
# PERCORRE AS DIV COLETANDO OS HORÁRIOS, MANDANTE DO JOGO E TIME VISITANTE
# SE A DIV NÃO ESTIVER VAZIA, O ELEMENTO É SALVO EM UM DICIONÁRIO E SALVA O DICIONÁRIO EM UMA LISTA PARA QUE POSSAMOS PEGAR OS DEMAIS VALORES
        dados.clear()
        if jogos.find(class_='CategoryHeader_stage__1lhRX') is not None:
            dados['campeonato'] = jogos.find(class_='CategoryHeader_stage__1lhRX').get_text()
        if jogos.find('span', class_='MatchRowTime_time__2Fkd2 MatchRowTime_justifyContentStart__3XvwU') is not None:
            dados['horario'] = jogos.find('span', class_='MatchRowTime_time__2Fkd2 MatchRowTime_justifyContentStart__3XvwU').get_text()
        if jogos.find(class_='FootballMatchRow_teamName__28Hxv') is not None:
            dados['time_casa'] = jogos.find(class_='FootballMatchRow_teamName__28Hxv').get_text()
        if jogos.find(class_='FootballMatchRow_away__12Br8') is not None:
            dados['time_fora'] = jogos.find(class_='FootballMatchRow_away__12Br8').get_text()
        lista.append(dados.copy())

# SALVA A LISTA DE DICIONÁRIOS COMO STR EM UM ARQUIVO .txt SE O DICIONÁRIO NÃO ESTIVER VAZIO
with open('tabela' + str(tomorrows_date) + '.txt', 'w', encoding="utf-8") as arquivo:
    for valor in lista:
        if bool(valor):
            arquivo.write(str(valor.values())+'\n')

# ABRE O ARQUIVO .txt E REMOVE OS CARACTERES EXCEDENTES PARA FICAR NO LIMITE DE 1600 CARACTERES DO TWILIO
with open('tabela' + str(tomorrows_date) + '.txt', 'r', encoding="utf-8") as arquivo2:
    data = arquivo2.read()
    # LISTA DE CARACTERES A SEREM REMOVIDOS
    caracteres_a_remover = ['dict_values([', '])']

    for x in range(len(data)):
        for y in range(len(caracteres_a_remover)):
            data = data.replace(caracteres_a_remover[y], "")

# PERGUNTA SE DEVE ENVIAR A TABELA DE JOGOS PELO WHATSAPP RESPEITANDO O LIMITE DE 1600 CARACTERES PERMITIDOS PELO TWILIO
def envia_whatsapp():
    resposta = input('Deseja enviar horário dos jogos para o whatsapp?[S/N]')
    if resposta in 'Ss':
        account_sid = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        auth_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_='whatsapp:+xxxxxxxxxxx',
            body=f'{str(data[:1599])}',
            to='whatsapp:+xxxxxxxxxx'
        )

        print(message.sid)
        print(data)
    else:
        print(data)


envia_whatsapp()
