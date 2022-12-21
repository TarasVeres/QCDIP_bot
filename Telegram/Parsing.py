# coding=utf-8
import json
import pprint

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

Sheet = dict()

def func_Access_id():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Access_id!A1:B200', majorDimension='ROWS').execute()
    Sheet['access_id'] = {}
    for i in _['values']:
        Sheet['access_id'][int(i[0])] = i[1]
    return Sheet

def func_Project():
    global Sheet, type, device
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Device!A1:C500', majorDimension='ROWS').execute()
    Sheet['project_all'] = {}
    for i in _['values']:
        try:
            if i[0] != '':
                type = i[0]
                Sheet['project_all'][type] = [] if i[1] == i[-1] else {}
            if (i[1] != '') and (i[1] == i[-1]):
                device = i[1]
                Sheet['project_all'][type] += [device]
            if (i[1] != '') and (i[1] != i[-1]):
                device = i[1]
                Sheet['project_all'][type][device] = [] if i[2] == i[-1] else {}
            if (i[2] != '') and (i[2] == i[-1]):
                project = i[2]
                Sheet['project_all'][type][device] += [project]
        except (IndexError, KeyError):
            pass
    return Sheet

def func_Spec():
    global Sheet, project
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Spec!A1:B2000', majorDimension='ROWS').execute()
    Sheet['spec'] = {}
    for i in _['values']:
        try:
            if i[0] != '':
                project = i[0]
                Sheet['spec'][project] = []
            if (i[1] != '') and (i[1] == i[-1]):
                specs = i[1]
                Sheet['spec'][project] += [specs]
        except (IndexError, KeyError):
            pass
    for i in Sheet['spec']:
        Sheet['spec'][i] += ['SMD']
        Sheet['spec'][i] += ['Інше']
    return Sheet

def func_Docs():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Docs!A2:C500', majorDimension='ROWS').execute()
    Sheet['docs'] = {}
    for i in _['values']:
        try:
            Sheet['docs'][i[0]] = [i[1], i[2]]
        except IndexError:
            pass
    return Sheet

def func_Defects():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Defects!A1:A50', majorDimension='ROWS').execute()
    Sheet['defects'] = []
    for i in _['values']:
        Sheet['defects'] += [i[0]]
    return Sheet

def func_DIP():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='DIP!A1:X50', majorDimension='COLUMNS').execute()
    Sheet['dip'] = {}
    for i in _['values']:
        try:
            if i[0] == '':
                i[0] = 'Без команди'
            i = [i[l] for l in range(len(i)) if i[l] != '']
            key = i[0].split(' ')
            key = f'{key[0]} {key[1][0]}. {key[2][0]}.'
            Sheet['dip'][key] = []
            for value in i:
                if len(value.split(' ')) > 2:
                    value = value.split(' ')
                    value = f'{value[0]} {value[1][0]}. {value[2][0]}.'
                    Sheet['dip'][key] += [value]
                else:
                    Sheet['dip'][key] += [value]
        except IndexError:
            pass
    return Sheet

def func_DIP_key():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='DIP!A1:X50', majorDimension='COLUMNS').execute()
    Sheet['dip_key'] = {}
    for i in _['values']:
        for l in i:
            try:
                if len(l.split(' ')) > 2:
                    values = l.split(' ')
                    values = f'{values[0]} {values[1][0]}. {values[2][0]}.'
                    Sheet['dip_key'][values] = l
                else:
                    Sheet['dip_key'][l] = l
            except IndexError:
                pass
    return Sheet

def func_telegram_teg():
    global Sheet
    _ = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range='Telegram_Teg!A1:B50', majorDimension='ROWS').execute()
    Sheet['telegram_teg'] = {}
    for i in _['values']:
        try:
            Sheet['telegram_teg'][i[0]] = i[1]
        except IndexError:
            pass
    return Sheet

def beginning():
    func_Access_id()
    func_Project()
    func_Spec()
    func_Defects()
    func_DIP()
    func_DIP_key()
    func_Docs()
    func_telegram_teg()
    with open("data_file.json", "w", encoding='utf8') as write_file:
        json.dump(Sheet, write_file, skipkeys=False, indent=4, ensure_ascii=False)
    return

beginning()