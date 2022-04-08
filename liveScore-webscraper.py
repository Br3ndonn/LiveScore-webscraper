from datetime import date, timedelta
from bs4 import BeautifulSoup
import requests
from twilio.rest import Client
import os

dados_partidas = dict()
lista_de_partidas = list()


def pega_url_com_data():
    """Pega a data desejada e concatena com a URL"""
    
    tomorrows_date = date.today() + timedelta(days=1)
    # today = "http://www.livescores.com/football/" + str(date.today()) + "/?tz=-3"
    next_day_url = "http://www.livescores.com/football/" + str(tomorrows_date) + "/?tz=-3"
    
    return next_day_url


def envia_whatsapp():
    """Envia a tabela de jogos pelo whatsapp se o usário desejar"""
    
    resposta = input('Deseja enviar horário dos jogos para o whatsapp?[S/N]')
    if resposta in 'Ss':
        account_sid = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        auth_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_='whatsapp:+xxxxxxxxxxx',
            body=f'{str(cria_arquivo_txt()[:1599])}',
            to='whatsapp:+xxxxxxxxxx'
        )

        print(message.sid)
        print(cria_arquivo_txt())
        deleta_arquivo_txt()
    else:
        print(cria_arquivo_txt())
        deleta_arquivo_txt()


def cria_arquivo_txt():
    with open('tabela' + str(f'{date.today() + timedelta(days=1)}') + '.txt', 'w', encoding="utf-8") as arquivo:
        for valor in lista_de_partidas:
            if bool(valor):
                arquivo.write(str(valor.values()) + '\n')

    with open('tabela' + str(f'{date.today() + timedelta(days=1)}') + '.txt', 'r', encoding="utf-8") as arquivo2:
        arquivo_txt = arquivo2.read()
        caracteres_a_remover = ['dict_values([', '])']

        for x in range(len(arquivo_txt)):
            for y in range(len(caracteres_a_remover)):
                arquivo_txt = arquivo_txt.replace(caracteres_a_remover[y], "")
                
    return arquivo_txt


def deleta_arquivo_txt():
    """Deleta o arquivo .txt gerado após lista de jogos ser exibida ao usuário"""
    
    nome_arquivo = 'tabela' + str(f'{date.today() + timedelta(days=1)}') + '.txt'
    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)
        

# REQUEST DO SITE
r = requests.get(pega_url_com_data())
soup = BeautifulSoup(r.content, 'html.parser')


# PERCORRE O CÓDIGO HTML EM BUSCA DOS ELEMENTOS DESEJADOS
for div in soup.find(class_='MatchRows_root__1NKae'):
    for partidas in div.find_all('div'):
# PERCORRE AS DIV COLETANDO OS HORÁRIOS, MANDANTE DO JOGO E TIME VISITANTE
# SE A DIV NÃO ESTIVER VAZIA, O ELEMENTO É SALVO EM UM DICIONÁRIO E SALVA O DICIONÁRIO EM UMA LISTA PARA QUE POSSAMOS PEGAR OS DEMAIS VALORES
        dados_partidas.clear()
        if partidas.find('span', class_='CategoryHeader_categoryHeaderWrapper__33fmX') is not None:
            dados_partidas['campeonato'] = partidas.find(class_='CategoryHeader_stage__1lhRX').get_text()
        if partidas.find('span', class_='MatchRowTime_time__2Fkd2 MatchRowTime_justifyContentStart__3XvwU') is not None:
            dados_partidas['horario'] = partidas.find('span', class_='MatchRowTime_time__2Fkd2 MatchRowTime_justifyContentStart__3XvwU').get_text()
        if partidas.find(class_='FootballMatchRow_teamName__28Hxv') is not None:
            dados_partidas['time_casa'] = partidas.find(class_='FootballMatchRow_teamName__28Hxv').get_text()
        if partidas.find(class_='FootballMatchRow_away__12Br8') is not None:
            dados_partidas['time_fora'] = partidas.find(class_='FootballMatchRow_away__12Br8').get_text()
        lista_de_partidas.append(dados_partidas.copy())

# SALVA A LISTA DE DICIONÁRIOS COMO STR EM UM ARQUIVO .txt SE O DICIONÁRIO NÃO ESTIVER VAZIO


envia_whatsapp()
