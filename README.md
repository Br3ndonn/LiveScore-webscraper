# LiveScore-webscraper

Webscraping do site de futebol LiveScore que monta uma tabela com todos os jogos de futebol do dia seguinte e envia para o seu WhatsApp usando a biblioteca Twilio.

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/LiveScore-webscraper.git
    cd LiveScore-webscraper
    ```

2. Crie um ambiente virtual (opcional) e ative-o:
    ```bash
    python -m venv venv
    venv\Scripts\activate  # No Windows
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. Configure suas credenciais do Twilio num arquivo `config.py`:
    ```python
    # config.py
    ACCOUNT_SID = 'your_account_sid'
    AUTH_TOKEN = 'your_auth_token'
    FROM_WHATSAPP_NUMBER = 'whatsapp:+14155238886'
    TO_WHATSAPP_NUMBER = 'whatsapp:+your_number'
    ```

2. Execute o script:
    ```bash
    python liveScore-webscraper.py
    ```

## Funcionalidades

- Webscraping do site LiveScore para obter jogos de futebol.
- Montagem de uma tabela com os jogos do dia seguinte.
- Envio da tabela para o WhatsApp usando a biblioteca Twilio.
- Pesquisa de jogos por time específico.
- Pesquisa de jogos por horário específico.
- Opção de deletar o arquivo `.txt` gerado.

# Usar o Twilio para enviar mensagens WhatsApp 
* Você precisa criar uma conta no Twilio e configurar algumas informações. Aqui estão os passos detalhados:

- Criar uma Conta no Twilio
Acesse o site do [Twilio](https://www.twilio.com/pt-br) e faça seu cadastro.
- Obter Credenciais da API
Acesse o Console do Twilio: Faça login na sua conta Twilio e vá para o Console.
Encontre o SID da Conta e o Token de Autenticação:
No painel do console, você verá o ACCOUNT SID e o AUTH TOKEN. Anote essas informações, pois você precisará delas para configurar seu script.
- Configurar o Sandbox do WhatsApp
Acesse o Sandbox do WhatsApp: No console do Twilio, vá para a seção de WhatsApp.
Configure o Sandbox:
Siga as instruções para configurar o Sandbox do WhatsApp. Você precisará enviar uma mensagem de teste para um número específico fornecido pelo Twilio para ativar o Sandbox.
Anote o número do WhatsApp fornecido pelo Twilio (FROM_WHATSAPP_NUMBER).
- Configurar o Script Python
Crie um arquivo config.py: No mesmo diretório do seu script liveScore-webscraper.py, crie um arquivo chamado config.py.

