from twilio.rest import Client
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
import time
import json

with open('credentials_twilio.json', 'r') as f:
    credentials = json.load(f)

with open('telefones.json', 'r') as f:
    telefones = json.load(f)
          
# Your Account Sid and Auth Token from twilio.com/console
account_sid = credentials['account_sid']
auth_token = credentials['auth_token']
client = Client(account_sid, auth_token)

def n_rows():

    scope = ['https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(credentials)
    sa = gspread.service_account('service_account.json')  

    name_sheet = 'Dashboard - Controle de OS'
    worksheet = 'Controle de OS'

    sh = sa.open(name_sheet)

    wks = sh.worksheet(worksheet)

    list1 = wks.get()
    table = pd.DataFrame(list1)

    table = table[table[1] != '']

    num_rows = len(table)

    return num_rows

num_rows = n_rows()

def n_rows_att():

    scope = ['https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    client = gspread.authorize(credentials)
    sa = gspread.service_account('service_account.json')  

    name_sheet = 'Dashboard - Controle de OS'
    worksheet = 'Controle de OS'

    sh = sa.open(name_sheet)

    wks = sh.worksheet(worksheet)

    list1 = wks.get()
    table = pd.DataFrame(list1)

    table = table[table[1] != '']

    num_rows = len(table)

    os = table.iloc[len(table)-1:len(table)].reset_index()[0][0]
    setor = table.iloc[len(table)-1:len(table)].reset_index()[3][0]
    data_hora = table.iloc[len(table)-1:len(table)].reset_index()[1][0] + ' ' + table.iloc[len(table)-1:len(table)].reset_index()[2][0]
    maquina = table.iloc[len(table)-1:len(table)].reset_index()[5][0]
    problema = table.iloc[len(table)-1:len(table)].reset_index()[6][0]

    body = "#### OS ABERTA! ####\
        \n\n--------------\n\nNúmero da OS: {}\
        \n\n--------------\n\nSetor: {}\
        \n\n--------------\n\nData de abertura: {}\
        \n\n--------------\n\nMáquina: {}\
        \n\n--------------\n\nProblema: {}".format(os, setor, data_hora, maquina, problema)

    return num_rows, body

interval = 30

lista_cels = telefones['telefones_pessoas']

while True:
    
    num_rows_att, body = n_rows_att()

    if num_rows_att > num_rows:

        for mess in range(len(lista_cels)):

            message = client.messages.create(
            from_='whatsapp:{}'.format(telefones['telefone_bot']),
            body=body,
            to='whatsapp:{}'.format(lista_cels[mess])
            )

        # atualizar o número de linhas
        num_rows = num_rows_att

    # esperar o intervalo de tempo antes de verificar novamente
    time.sleep(interval)