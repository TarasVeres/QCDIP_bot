import time
from run_json import *

Sheet = checker()

def assembling(c_id):
    global Sheet
    post = f'''{time.strftime("%d.%m.%Y", time.localtime())}\n''' \
           f'''Локація: {c_id['locations']}, {c_id['floor']}'''
    if 'non_distric' not in c_id['distric']:
        post += f'''\nДільниця генератор невідповідності: {c_id['distric']}'''
    if 'kl' in c_id:
        post += f''', {c_id['kl']}''' if 'Без КЛ' not in c_id['kl'] else ''
    if 'kl_rm' in c_id:
        post += f''' {c_id['kl_rm']}''' if 'Без р.м.' not in c_id['kl_rm'] else ''
    post += '' if 'non_distric' in c_id['distric'] else ''
    if 'room' in c_id:
        if ("Без роб місця" not in c_id['room']) and ("Без КЛ" not in c_id['room']) and ("Без р.м." not in c_id['room']):
            post += f''', {c_id['room']}''' if 'room' in c_id else ''
    if 'projects' not in c_id:
        if ('device' in c_id) and ('Без девайсу' in c_id['device']):
            post += ''
        elif ('device' in c_id) and (c_id['device'] in Sheet['Kit']):
            post += f'''\nKit: {c_id['device']}'''
        else:
            post += f'''\nДевайс: {c_id['device']}''' if 'device' in c_id else ''
    if 'projects' in c_id:
        post += f'''\nПроект: {c_id['projects']}'''
    if 'Sp' in c_id:
        post += f'''\nПовідомлений(на): {c_id['Sp']}'''
    post += f'''\nНевідповідність: {c_id['report']}''' \
            f'''\nГрупа виявленої невідповідності: {c_id['group']}''' \
            f'''\nЗафіксував(ла): {c_id['record']}'''
    return post
