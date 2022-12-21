# coding=utf-8
import time
import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'
spreadsheet_id = '12gvu_yxTqLfIPNo-T8unIhaz4AoAevydHy4EM1vb0Ig'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

day = 32
number = 1

def number_writer():
    global day, number
    if day != time.localtime().tm_mday:
        _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Print!A1:A21000', majorDimension='COLUMNS').execute()
        number = int(_['values'][-1][-1]) if _['values'][-1][-1] != '№' else 1
        day = time.localtime().tm_mday
    return number

def writer_languages(record, Sheet, callc):
    num = Sheet['Access_id_language'][record][0][0]
    values = [[] for i in range(4)]
    values[0] = [num]
    values[1] = [Sheet['Access_id_language'][record][1]]
    values[2] = [Sheet['Access_id_language'][record][2]]
    values[3] = [callc]
    value = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f'Access_id_lang!A{num}:D100',
                 "majorDimension": "COLUMNS",
                 "values": values}
            ]
        }
    ).execute()

def writer(c_id):
    global number
    number += 1
    value = [[''] for i in range(11)]
    value[0] = [str(number)]
    value[1] = [time.strftime("%d.%m.%Y", time.localtime())]
    value[2] = [c_id['locations']]
    value[3] = [c_id['floor'] if 'non_distric' in c_id['distric'] else '']
    if 'non_distric' not in c_id['distric']:
        count_floor = ' №1' if c_id['floor'] in 'Поверх 1' else ' №2'
        value[3] = [c_id['distric'] + count_floor]
    if 'room' in c_id:
        value[4] = [c_id['room'] if (('Без КЛ' not in c_id['room']) and ('Без р.м.' not in c_id['room'])) else '']
    if 'kl' in c_id:
        value[4] = [c_id['kl'] + ' ' + c_id['kl_rm'] if c_id['kl_rm'] not in 'Без р.м.' else c_id['kl']]
    if ('type' in c_id) and (c_id['type'] in 'Без девайсу'):
        value[5] = ['']
    elif 'kit' in c_id:
        value[5] = [c_id['device']]
    else:
        value[5] = [c_id['projects'] if 'projects' in c_id else c_id['device']]
    value[6] = [c_id['Sp'] if 'Sp' in c_id else '']
    value[7] = [c_id['group']]
    value[8] = [c_id['report']]
    value[9] = [c_id['record']]
    value[10] = [c_id['text']]
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {"range": f'Print!A{number}:K21000',
                 "majorDimension": "COLUMNS",
                 "values": value}
            ]
        }
    ).execute()


def print_text(c_id, count, Sheet):
    tel = Sheet['languages'][str(count)][c_id['language']]
    return tel