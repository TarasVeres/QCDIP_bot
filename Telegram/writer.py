# coding=utf-8
import time
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '1Gki5lGMO4nI7ZnwNP4XTNK9Rzjp8x77HIFTLkB77kDw'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

number = 1

def update_number_writer():
    global day, number
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Print!A1:A21000', majorDimension='COLUMNS').execute()
    number = int(_['values'][-1][-1]) if _['values'][-1][-1] != '№' else 1
    return number

def writer(c_id, Sheet):
    global number
    value = [[''] for _ in range(25)]
    value[0] = [str(update_number_writer() + 1)]
    value[1] = [time.strftime("%d.%m.%Y", time.localtime())]
    value[2] = [time.strftime("%H:%M", time.localtime())]
    value[3] = [c_id['project']]
    value[4] = [Sheet['dip_key'][c_id['dip']]]
    value[6] = [c_id['number_boards']]
    if 'repair' in c_id:
        value[22] = [c_id['non_liquidity']]
        value[23] = [c_id['repair']]
        value[24] = [c_id['reported']]
        for i in c_id['writer_stack']:
            defects = {
                    "Невірна полярність": 7,
                    "Нахил": 8,
                    "Відсутність компонента": 9,
                    "Проміжок": 10,
                    "Холодна пайка": 11,
                    "Залишки": 12,
                    "Непропай": 13,
                    "Коротке замикання": 14,
                    "Запаяний тест поінт": 15,
                    "КЗ на SMD": 16,
                    "Пошкодження маски": 17,
                    "Пошкодження плати": 18,
                    "Неліквід компонента": 19,
                    "Невірна формовка": 20,
                    "Інші або Примітка": 21
            }
            if value[defects[i[0]]] != ['']:
                value[defects[i[0]]][0] += f'/{i[1]}-{i[2]}'
            else:
                value[defects[i[0]]] = [f'{i[1]}-{i[2]}']
    else:
        value[22] = [0]
        value[23] = [0]
        value[24] = [c_id['reported']]
    value[5] = [int(*value[6]) - int(*value[23])]
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f'Print!A{number + 1}:Y21000',
                 "majorDimension": "COLUMNS",
                 "values": value}
            ]
        }
    ).execute()


def writer_blocked(c_id, Sheet):
    global number
    number += 1
    value = [[''] for i in range(25)]
    value[0] = [str(number)]
    value[1] = [time.strftime("%d.%m.%Y", time.localtime())]
    value[2] = [time.strftime("%H:%M", time.localtime())]
    value[3] = [c_id['project']]
    value[4] = [Sheet['dip_key'][c_id['dip']]]
    value[6] = [c_id['number_boards']]
    value[22] = [0]
    value[23] = [c_id['number_boards']]
    value[24] = ['Контролер']
    value[5] = [int(*value[6]) - int(*value[23])]
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f'Print!A{update_number_writer() + 1}:Y21000',
                 "majorDimension": "COLUMNS",
                 "values": value}
            ]
        }
    ).execute()