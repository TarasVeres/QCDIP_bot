# coding=utf-8
import time

def assembling(c_id, Sheet):
    try:
        post = f'''{time.strftime("%d.%m.%Y %H:%M", time.localtime())}\n''' \
               f'''Монтажник: #{Sheet['dip_key'][c_id['dip']]}\n'''\
               f'''Проект: {c_id['project']}\n'''\
               f'''Перевірено: {c_id['number_boards']}\n'''\
               f'''Неліквідні: {c_id['non_liquidity']}\n''' \
               f'''На ремонт: {c_id['repair']}\n''' \
               f'''Контролер: {c_id['reported']}'''
    except KeyError:
        post = f'''{time.strftime("%d.%m.%Y %H:%M", time.localtime())}\n''' \
               f'''Монтажник: #{Sheet['dip_key'][c_id['dip']]}\n''' \
               f'''Проект: {c_id['project']}\n''' \
               f'''Перевірено: {c_id['number_boards']}\n''' \
               f'''Контролер: {c_id['reported']}'''
    return post

def assembling_defect(m_id):
    assembliator = f'''Дефект: {m_id['defect']}\n'''\
                  f'''Компонент: {m_id['component']}\n'''\
                  f'''Кількість: {m_id['amount']}\n'''\
                  f'''__________\n'''
    writer_defect(m_id)
    return assembliator

def assembling_spec(project, Sheet):
    try:
        maps = f'''<a href='{Sheet['docs'][project][0]}'><b>Карта пайки</b></a>'''
        spec = f'''<a href='{Sheet['docs'][project][1]}'><b>Специфікація</b></a>'''
        assembling = 'Оберіть компонент на якому виявлено дефект\n' \
                        f'{maps}                {spec}'
    except KeyError:
        assembling = 'Оберіть компонент на якому виявлено дефект\n'
    return assembling


def assembling_finished(c_id, Sheet):
    post = assembling(c_id, Sheet)
    post += '\n__________\n'
    post += c_id['stack_defects']
    return post

def writer_defect(m_id):
    m_id['writer_stack'].append([m_id['defect'], m_id['component'], m_id['amount']])
    return m_id

def assembling_blocked(m_id, Sheet):
    try:
        post = f'''{time.strftime("%d.%m.%Y %H:%M", time.localtime())}\n''' \
           f'''#ЗАБЛОКОВАНО\n'''\
           f'''Монтажник: #{Sheet['dip_key'][m_id['dip']]}\n'''\
           f'''Проект: {m_id['project']}\n'''\
           f'''Кількість: {m_id['number_boards']}\n''' \
           f'''Дефект: {m_id['blocked']}\n'''\
           f'''Контролер: {m_id['reported']}\n'''\
           f'''{Sheet['telegram_teg']['Відповідальний за QCDIP']} {Sheet['telegram_teg']['Відповідальний за DIP']}
{Sheet['telegram_teg'][Sheet['dip_key'][m_id['team']]]}'''
    except KeyError:
        post = f'''{time.strftime("%d.%m.%Y %H:%M", time.localtime())}\n''' \
               f'''#ЗАБЛОКОВАНО\n''' \
               f'''Монтажник: #{Sheet['dip_key'][m_id['dip']]}\n''' \
               f'''Проект: {m_id['project']}\n''' \
               f'''Кількість: {m_id['number_boards']}\n''' \
               f'''Дефект: {m_id['blocked']}\n''' \
               f'''Контролер: {m_id['reported']}\n'''\
               f'''{Sheet['telegram_teg']['Відповідальний за QCDIP']} {Sheet['telegram_teg']['Відповідальний за DIP']}'''
    return post



input_validation_project = (f'Введено невірні данні\n\n'
                            f'✅Tільки числа\n'
                            f'✅Кількість від 0 до 1500\n\n'
                            f'❌Заборонено вводити літери\n'
                            f'❌Заборонено вводити десяткові цифри\n'
                            f'❌Заборонено вводити кількість менше 0 та більше 1500 за один запис')

input_validation_defect = (f'Введено невірні данні\n\n'
                           f'✅Tільки числа\n'
                           f'✅Кількість від 0 до 500\n\n'
                           f'❌Заборонено вводити літери\n'
                           f'❌Заборонено вводити десяткові цифри\n'
                           f'❌Заборонено вводити кількість менше 0 та більше 500 за один запис')