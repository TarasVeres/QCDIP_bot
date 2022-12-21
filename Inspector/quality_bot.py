# coding=utf-8

from aiogram import Bot, Dispatcher, types, executor

import writer
import Deleter
import Inline_Keyboard
import assembler_message
from run_json import checker, starter, update_sheet

Token_work = '5388966053:AAE6rJo_7wbBbGDMG3QntbjN549Ym1lyEgY'
Chat_work = '-1001286473377'

Token_test = '5182014508:AAEBytjLM9Gu-3F2o1Qc2QPt5bwdvNWxFEk'
Chat_test = '-1001626029923'

bot = Bot(Token_test, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
Reply_message = dict()
mq = str()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global Sheet
    Sheet = checker()
    if message.chat.id == message.from_user.id:
        if str(message.chat.id) in Sheet['Access_id']:
            await bot.send_message(message.chat.id, starter)
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.message_handler(commands=['updatesheet'])
async def UpdateSheet(message: types.Message):
    if message.chat.id == message.from_user.id:
        Sheet = update_sheet()
        if str(message.from_user.id) in Sheet['Access_id']:
            await bot.send_message(chat_id=message.chat.id, text='Данні з таблиці оновлено.')
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.message_handler(content_types=['video', 'photo'])
async def start_function(message: types.Message):
    global Reply_message, mq, Sheet, m_id
    Sheet = checker()
    writer.number_writer()
    if message.chat.id == message.from_user.id:
        if str(message.chat.id) in Sheet['Access_id']:
            if mq == '':
                m_id = message.chat.id
                Reply_message[m_id] = dict()
                Reply_message[m_id]['text'] = ''
                Reply_message[m_id]['photos'] = []
                Reply_message[m_id]['videos'] = []
                Reply_message[m_id]['med'] = []
                Reply_message[m_id]['Back'] = 'Back'
            location = [i for i in Sheet['Location']]
            button = Inline_Keyboard.inline_c2_home(location)
            button.add(types.InlineKeyboardButton(text='Змінити фото/відео', callback_data='new_photo'))
            try:
                Reply_message[m_id]['photos'].append(message.photo[0].file_id)
            except (KeyError, IndexError):
                pass
            try:
                Reply_message[m_id]['videos'].append(message.video.file_id)
            except AttributeError:
                pass
            if mq == '':
                mq = message.media_group_id
                await bot.send_message(message.chat.id, 'На якій локації зафіксовано невідповідність?', reply_markup=button)
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.callback_query_handler(lambda callback_query: True)
async def device_callback(call: types.CallbackQuery):
    global mq, Reply_message, backer
    button = types.InlineKeyboardMarkup(row_width=2)
    try:
        mq = ''
        c_id = call.from_user.id
        Reply_message[c_id]['stoper'] = 'good'
        if (call.data in Sheet['Location']) and not Sheet['Location'][call.data]:
            await call.answer(f'Локація: {call.data}')
            button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='Back'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Локація ще будується!',
                                        reply_markup=button)
        elif call.data in 'new_photo':
            await call.answer('')
            mq = ''
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Надішліть фото/відео')
        elif call.data in 'Back':
            await call.answer(text='')
            location = [i for i in Sheet['Location']]
            button = Inline_Keyboard.inline_c2_home(location)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='На якій локації зафіксовано невідповідність?', reply_markup=button)
        elif call.data in Sheet['Location']:
            await call.answer(f'Локація: {call.data}')
            delete = ['distric', 'floor', 'room', 'locations', 'device', 'projects', 'kl', 'kl_rm', 'Sp', 'type', 'report', 'kit']
            Deleter.deleter_key(delete, Reply_message[c_id])
            Reply_message[c_id]['locations'] = call.data
            Floor = [i for i in Sheet['Location'][Reply_message[c_id]['locations']]]
            button = Inline_Keyboard.inline_c2(Floor, 'Back', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=Reply_message[c_id]['locations'], reply_markup=button)
        elif (call.data in Sheet['Location'][Reply_message[c_id]['locations']]) and (call.data not in Sheet['Non_standart']) and (
                call.data not in Sheet['Storage']):
            await call.answer(text=f'Поверх: {call.data}')
            deleter = ['distric', 'floor', 'room', 'device', 'projects', 'kl', 'kl_rm', 'Sp', 'type', 'report', 'kit']
            Deleter.deleter_key(deleter, Reply_message[c_id])
            Reply_message[c_id]['floor'] = call.data
            Districs = [i for i in Sheet['Location'][Reply_message[c_id]['locations']][Reply_message[c_id]['floor']]]
            button = Inline_Keyboard.inline_c2(Districs, 'locations', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Дільниця генератор '
                                                                                                               'невідповідності:',
                                        reply_markup=button)
        elif call.data in 'Production Warehouse':
            await call.answer(text=call.data)
            delete = ['room', 'device', 'projects', 'kl', 'kl_rm', 'Sp', 'type', 'report', 'kit']
            Reply_message[c_id] = Deleter.deleter_key(delete, Reply_message[c_id])
            Reply_message[c_id]['floor'] = call.data
            Reply_message[c_id]['distric'] = 'non_distric'
            button = types.InlineKeyboardMarkup(row_width=2)
            button.add(
                types.InlineKeyboardButton(text='Девайс', callback_data='Девайс'),
                types.InlineKeyboardButton(text='Kit', callback_data='Ajax_Kit')
            )
            button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=Reply_message[c_id]['locations']))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=Reply_message[c_id]['floor'],
                                        reply_markup=button)
        elif call.data in 'Ajax_Kit':
            await call.answer(text=call.data)
            delete = ['room', 'device', 'projects', 'kl', 'kl_rm', 'Sp', 'type', 'report', 'kit']
            Reply_message[c_id] = Deleter.deleter_key(delete, Reply_message[c_id])
            Reply_message[c_id]['kit'] = call.data
            backer = 'floor'
            kit = [i for i in Sheet['Kit']]
            button = Inline_Keyboard.inline_c2(kit, backer, Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Kit', reply_markup=button)
        elif ((call.data in Sheet['Storage']) and (call.data not in 'Production Warehouse')) or (call.data in Sheet['Non_standart']) \
            or (call.data in 'Девайс') or (call.data in Sheet['Non_place']):
            await call.answer(text=call.data)
            delete = ['room', 'device', 'projects', 'kl', 'kl_rm', 'Sp', 'type', 'report', 'kit']
            Reply_message[c_id] = Deleter.deleter_key(delete, Reply_message[c_id])
            if call.data in Sheet['Storage']:
                Reply_message[c_id]['floor'] = call.data
                Reply_message[c_id]['distric'] = 'non_distric'
            if (call.data in Sheet['Non_place']) or (call.data in Sheet['Non_standart']):
                Reply_message[c_id]["distric"] = call.data
            backer = 'locations' if Reply_message[c_id]['distric'] == 'non_distric' else 'floor'
            devic = [i for i in Sheet['Device']]
            button = Inline_Keyboard.inline_c2(devic, backer, Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Лінійка девайсів:',
                                        reply_markup=button)
        elif (call.data in Sheet['Room']) or (call.data in Sheet['KL_line']):
            await call.answer(text=f'Дільниця генератор невідповідності: {call.data}')
            delete = ['distric', 'room', 'device', 'projects', 'kl', 'kl_rm', 'Sp', 'type', 'report', 'kit']
            Deleter.deleter_key(delete, Reply_message[c_id])
            Reply_message[c_id]["distric"] = call.data
            if 'non_project' in Sheet['Location'][Reply_message[c_id]["locations"]][Reply_message[c_id]["floor"]][Reply_message[c_id]["distric"]]:
                place = [i for i in Sheet['Location'][Reply_message[c_id]["locations"]][Reply_message[c_id]["floor"]][Reply_message[c_id]["distric"]]['non_project']]
            else:
                place = [i for i in Sheet['Location'][Reply_message[c_id]["locations"]][Reply_message[c_id]["floor"]][Reply_message[c_id]["distric"]]]
            button = Inline_Keyboard.inline_c2(place, 'floor', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{Reply_message[c_id]["distric"]}:', reply_markup=button)
        elif (('type' in Reply_message[c_id]) and (Reply_message[c_id]['type'] not in 'Ajax_Kit')) and (call.data in Sheet['Device'][Reply_message[c_id]['type']]) and ('non_project'
            not in Sheet['Location'][Reply_message[c_id]["locations"]][Reply_message[c_id]["floor"]][Reply_message[c_id]["distric"]]) and (call.data not in 'Без девайсу'):
            await call.answer(text=call.data)
            delete = ['projects', 'Sp', 'report']
            Deleter.deleter_key(delete, Reply_message[c_id])
            Reply_message[c_id]["device"] = call.data
            project = [i for i in Sheet['Device'][Reply_message[c_id]["type"]][Reply_message[c_id]["device"]]]
            button = Inline_Keyboard.inline_c1(project, 'type', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Проект:',
                                        reply_markup=button)
        elif ((Reply_message[c_id]['distric'] in Sheet['Room']) or (Reply_message[c_id]['distric'] in Sheet['KL_line'])) and ((call.data in Sheet['Location'][Reply_message[c_id][
            'locations']][Reply_message[c_id]['floor']][Reply_message[c_id]['distric']]) or (('non_project' in Sheet['Location'][Reply_message[c_id]['locations']][Reply_message[c_id]['floor']][Reply_message[c_id][
            'distric']]) and (call.data in Sheet['Location'][Reply_message[c_id]['locations']][Reply_message[c_id]['floor']][Reply_message[c_id]['distric']]['non_project']))) and \
            (not call.data.startswith('КЛ')):
            await call.answer(text=f'{Reply_message[c_id]["distric"]}: {call.data}')
            delete = ['device', 'projects', 'Sp', 'type', 'report']
            Deleter.deleter_key(delete, Reply_message[c_id])
            Reply_message[c_id]["room"] = call.data
            devic = [i for i in Sheet['Device']]
            button = Inline_Keyboard.inline_c2(devic, 'distric', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Лінійка девайсів:',
                                        reply_markup=button)
        elif call.data.startswith('КЛ'):
            await call.answer(text=f'{Reply_message[c_id]["distric"]}: {call.data}')
            Reply_message[c_id]['kl'] = call.data
            button = Inline_Keyboard.inline_c2(Sheet['KL_R_M'], 'distric', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=Reply_message[c_id]['kl'],
                                        reply_markup=button)
        elif (call.data in Sheet['KL_R_M']) or (call.data in 'Без р.м.'):
            await call.answer(text=f"{Reply_message[c_id]['kl']}: {call.data}")
            Reply_message[c_id]['kl_rm'] = call.data
            delete = ['device', 'projects', 'Sp', 'type', 'report']
            Deleter.deleter_key(delete, Reply_message[c_id])
            devic = [i for i in Sheet['Device']]
            button = Inline_Keyboard.inline_c2(devic, 'kl', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Лінійка девайсів:',
                                        reply_markup=button)
        elif (Reply_message[c_id]["floor"] not in 'Control Unpacking') and ((('type' in Reply_message[c_id]) and ('kit' not in Reply_message[c_id])) and (call.data in Sheet[
            'Device'][Reply_message[c_id]['type']])) or ((call.data in 'Без девайсу') and (Reply_message[c_id]["floor"] not in 'Control Unpacking')) or (call.data in
                                                                                                                           Sheet['Kit']):
            await call.answer(text=call.data)
            if (call.data not in 'Без девайсу') and (call.data not in Sheet['Kit']):
                Reply_message[c_id]['device'] = call.data
            elif call.data in Sheet['Kit']:
                Reply_message[c_id]['device'] = call.data
            else:
                Reply_message[c_id]['type'] = call.data
            delete = ['Sp', 'report']
            Deleter.deleter_key(delete, Reply_message[c_id])
            backer = 'floor' if ((('type' in Reply_message[c_id]) and (Reply_message[c_id]['type'] in 'Без девайсу') and ('kl_rm' not in Reply_message[c_id])) or ((Reply_message[c_id]['floor'] in
                    Sheet['Storage']) and (('type' in Reply_message[c_id]) and ((Reply_message[c_id]['type']) in 'Без девайсу')))) else 'kl'
            backer = 'kit' if 'kit' in Reply_message[c_id] else backer
            backer = 'distric' if ((('type' in Reply_message[c_id]) and (Reply_message[c_id]['type'] in 'Без девайсу') and Reply_message[c_id]['distric'] not in 'non_distric') or ((('room' in Reply_message[c_id]) or
                    ((Reply_message[c_id]['distric'] in Sheet['Non_standart']) and (Reply_message[c_id]['type'] in 'Без девайсу'))) and (
                    Reply_message[c_id]['distric'] not in Sheet['Storage']) and ('distric' in Reply_message[c_id]))) else backer
            backer = 'room' if (('room' in Reply_message[c_id]) and ('device' not in Reply_message[c_id])) else backer
            backer = 'kl_rm' if (('kl_rm' in Reply_message[c_id]) and (Reply_message[c_id]['kl'] not in 'Без КЛ')) else backer
            backer = 'type' if (('type' in Reply_message[c_id]) and ((('kl_rm' in Reply_message[c_id]) or (Reply_message[c_id]['distric']
                in Sheet['Non_standart']) or (Reply_message[c_id]['floor'] in Sheet['Storage'])) and (Reply_message[c_id]['type'] not in
                'Без девайсу')) or ('room' in Reply_message[c_id]) and (('type' in Reply_message[c_id])
                and (Reply_message[c_id]['type'] not in 'Без девайсу'))) else backer
            if Reply_message[c_id]["distric"] in 'non_distric':
                sp = [i for i in Sheet['SP'][Reply_message[c_id]["locations"]][Reply_message[c_id]["floor"]]]
            else:
                sp = [i for i in Sheet['SP'][Reply_message[c_id]["locations"]][Reply_message[c_id]['distric']]]
            button = Inline_Keyboard.inline_c1(sp, backer, Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Повідомлений(на):',
                                        reply_markup=button)
        elif ((Reply_message[c_id]['floor'] in Sheet['Storage']) and (Reply_message[c_id]['floor'] not in 'Control Unpacking')) and \
            (call.data in Sheet['SP'][Reply_message[c_id]['locations']][Reply_message[c_id]['floor']]) and (call.data not in 'Відсутній в списку'):
            await call.answer(text=f'Повідомлений(на):{call.data}')
            Reply_message[c_id]['Sp'] = call.data
            backer = 'device' if 'device' in Reply_message[c_id] else 'floor'
            backer = 'projects' if 'projects' in Reply_message[m_id] else backer
            backer = 'type' if ('type' in Reply_message[c_id]) and (Reply_message[c_id]['type'] in 'Без девайсу') else backer
            group = [i for i in Sheet['Group']]
            button = Inline_Keyboard.inline_c1(group, backer, Reply_message[m_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Оберіть групу виявленої '
                                                     'невідповідності:', reply_markup=button)
        elif ((Reply_message[c_id]["floor"] in 'Control Unpacking') and (('type' in Reply_message[c_id]) and ('device' not in
            Reply_message[c_id])) or ((Reply_message[c_id]["floor"] in 'Control Unpacking') and (call.data in 'Без девайсу'))) \
                or ('Back2' in Reply_message[c_id]['Back']) and (call.data not in 've_chat') and  (call.data not in 'no_ve_chat'):
            if call.data in 'Без девайсу':
                await call.answer(text=call.data)
                Reply_message[c_id]['type'] = call.data
            elif call.data in Sheet['Device'][Reply_message[c_id]['type']]:
                await call.answer(text=f'Девайс: {call.data}')
            if call.data not in Sheet['Group']:
                Reply_message[c_id]["device"] = call.data
            Reply_message[c_id]['Back'] = 'Back'
            backer = 'floor' if Reply_message[c_id]['type'] in 'Без девайсу' else 'type'
            group = [i for i in Sheet['Group']]
            button = Inline_Keyboard.inline_c1(group, backer, Reply_message[m_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Оберіть групу виявленої'
                                                   ' невідповідності:', reply_markup=button)
        elif (('type' in Reply_message[c_id]) and (Reply_message[c_id]['type'] not in 'Без девайсу')) and (call.data not in 've_chat') \
                and (call.data not in 'no_ve_chat') and ('device' in Reply_message[c_id]) and (call.data in Sheet['Device']
                [Reply_message[c_id]['type']][Reply_message[c_id]['device']]):
            await call.answer(text=f'Проект: {call.data}')
            delete = ['projects', 'Sp', 'report']
            Deleter.deleter_key(delete, Reply_message[c_id])
            Reply_message[c_id]["projects"] = call.data
            sp = [i for i in Sheet['SP'][Reply_message[c_id]["locations"]][Reply_message[c_id]["distric"]]]
            button = Inline_Keyboard.inline_c1(sp, 'device', Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Повідомлений(на):',
                                        reply_markup=button)
        elif (call.data in Sheet['Device']) and (call.data not in 'Без девайсу'):
            await call.answer(text=call.data)
            Reply_message[c_id]['type'] = call.data
            delete = ['device']
            Deleter.deleter_key(delete, Reply_message[c_id])
            backer = 'room' if 'room' in Reply_message[c_id] else 'distric'
            backer = 'floor' if Reply_message[c_id]['distric'] in 'non_distric' else backer
            backer = 'kl_rm' if 'kl_rm' in Reply_message[c_id] else backer
            devic = [i for i in Sheet['Device'][Reply_message[c_id]['type']]]
            button = Inline_Keyboard.inline_c2(devic, backer, Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Девайс:',
                                        reply_markup=button)
        elif (Reply_message[c_id]["floor"] not in Sheet['Storage']) and (Reply_message[c_id]["floor"] not in Sheet['Non_standart']) and (
            call.data in Sheet['SP'][Reply_message[c_id]["locations"]][Reply_message[c_id]["distric"]]) and (call.data not in 'Відсутній в списку'):
            await call.answer(text=f'Повідомлений(на): {call.data}')
            Reply_message[c_id]["Sp"] = call.data
            backer = 'type' if Reply_message[c_id]['type'] in 'Без девайсу' else 'device'
            backer = 'projects' if 'projects' in Reply_message[m_id] else backer
            group = [i for i in Sheet['Group']]
            button = Inline_Keyboard.inline_c1(group, backer, Reply_message[m_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Оберіть групу виявленої'
                                                                        ' невідповідності:', reply_markup=button)
        elif call.data in 've_chat':
            await call.answer(text='Повідомлення успішно переслане!')

            await bot.send_media_group(chat_id=Chat_work, media=Reply_message[c_id]['med'])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Повідомлення успішно '
                                                                                                               'переслане!')
            writer.writer(Reply_message[c_id])
            Reply_message.pop(c_id)
        elif call.data in 'no_ve_chat':
            await call.answer()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Залишимо це повідомлення тут.')
            Reply_message.pop(c_id)
        elif call.data in 'Відсутній в списку':
            await call.answer()
            Reply_message[c_id]['Sp'] = 'None'
            backer = 'type' if (('type' in Reply_message[c_id]) and (Reply_message[c_id]['type'] in 'Без девайсу')) else 'projects'
            backer = 'device' if ((('non_project' in Sheet['Location'][Reply_message[c_id]['locations']][Reply_message[c_id]['floor']]
            [Reply_message[c_id]['distric']]) or (Reply_message[c_id]['floor'] in Sheet['Storage'])) and ('type' in Reply_message[c_id])
            and (Reply_message[c_id]['type'] not in 'Без девайсу')) or ('kit' in Reply_message[c_id]) else backer
            button.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=Reply_message[c_id][backer]))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text='Введіть ПІБ працівника повідомленого про невідповідність:', reply_markup=button)
        elif call.data in Sheet['Group']:
            await call.answer(call.data)
            Reply_message[c_id]['group'] = call.data
            Reply_message[c_id]['med'] = []
            backer = Reply_message[c_id]['Sp'] if Reply_message[c_id]['floor'] not in 'Control Unpacking' else Reply_message[c_id]['device']
            if (('Sp' in Reply_message[c_id]) and (Reply_message[c_id]['Sp'] in backer)) and ((('non_distric' not in Reply_message[c_id]
                ['distric']) and (Reply_message[c_id]['Sp'] not in Sheet['SP'][Reply_message[c_id]['locations']][Reply_message[c_id]
                ['distric']])) or (('non_distric' in Reply_message[c_id]['distric']) and (Reply_message[c_id]['Sp'] not in
                Sheet['SP'][Reply_message[c_id]['locations']][Reply_message[c_id]['floor']]))):
                backer = 'Відсутній в списку'
            if Reply_message[c_id]['floor'] in 'Control Unpacking':
                Reply_message[c_id]['Back'] = 'Back2'
            button.add(types.InlineKeyboardButton('⬅️ Назад', callback_data=backer))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Опишіть невідповідність:',
                                        reply_markup=button)
    except (IndexError, KeyError):
        pass

@dp.message_handler(content_types=['text'])
async def handle_files(message):
    if message.chat.id == message.from_user.id:
        if str(message.chat.id) in Sheet['Access_id']:
            global Reply_message, mq
            try:
                m_id = message.chat.id
                Reply_message[m_id]['med'] = []
                if ('Control Unpacking' not in Reply_message[m_id]['floor']) and ('None' in Reply_message[message.chat.id]['Sp']):
                    Reply_message[Inline_Keyboard.func_message(message)[0]]['Sp'] = Inline_Keyboard.func_message(message)[1]
                    backer = 'projects' if 'projects' in Reply_message[m_id] else 'device'
                    backer = 'type' if (('type' in Reply_message[m_id]) and (Reply_message[m_id]['type'] in 'Без девайсу')) else backer
                    group = [i for i in Sheet['Group']]
                    button = Inline_Keyboard.inline_c1(group, backer, Reply_message[m_id])
                    await bot.send_message(message.chat.id, text='Оберіть групу виявленої невідповідності:', reply_markup=button)
                else:
                    Reply_message[Inline_Keyboard.func_message(message)[0]]['report'] = Inline_Keyboard.func_message(message)[1]
                    Reply_message[m_id]['record'] = Sheet['Access_id'][str(m_id)]
                    if 'group' in Reply_message[m_id]:
                        Reply_message[Inline_Keyboard.func_message(message)[0]]['text'] = assembler_message.assembling(
                                Reply_message[Inline_Keyboard.func_message(message)[0]])
                    for i in Reply_message[m_id]['photos']:
                        if i != Reply_message[m_id]['photos'][-1]:
                            Reply_message[m_id]['med'].append(types.InputMediaPhoto(media=i))
                        else:
                            Reply_message[m_id]['med'].append(types.InputMediaPhoto(media=i, caption=Reply_message[m_id]['text']))
                    for i in Reply_message[m_id]['videos']:
                        if Reply_message[m_id]['photos']:
                            Reply_message[m_id]['med'].append(types.InputMediaVideo(media=i))
                        else:
                            if i != Reply_message[m_id]['videos'][-1]:
                                Reply_message[m_id]['med'].append(types.InputMediaVideo(media=i))
                            else:
                                Reply_message[m_id]['med'].append(types.InputMediaVideo(media=i, caption=Reply_message[m_id]['text']))
                    button = types.InlineKeyboardMarkup(row_width=2)
                    button.add(types.InlineKeyboardButton(text='Так', callback_data='ve_chat'), types.InlineKeyboardButton(text='Ні',
                                                                                                                callback_data='no_ve_chat'))
                    button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=Reply_message[m_id]['group']))
                    if 'text' in Reply_message[m_id]:
                        if 'stop' not in Reply_message[m_id]['stoper']:
                            await bot.send_media_group(message.chat.id, media=Reply_message[m_id]['med'])
                            await bot.send_message(message.chat.id, 'Переслати повідомлення в чат невідповідностей?', reply_markup=button)
                            Reply_message[m_id]['stoper'] = 'stop'
            except (KeyError, IndexError):
                pass
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=False)