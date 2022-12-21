# coding=utf-8
import pprint

from aiogram import Dispatcher, Bot, types, executor

import assembler_message
from run_json import checker, update_sheet
import writer
import Inline_Keyboard

Token_test = '5182014508:AAEBytjLM9Gu-3F2o1Qc2QPt5bwdvNWxFEk'
Token_work = '5558069507:AAGPrltIj5K_1tj85ULWew8x190Y7dUXoPk'

Chat_test = '-1001626029923'
Chat_work = '-1001673810175'

bot = Bot(Token_test)
dp = Dispatcher(bot)
Reply_message = dict()
mq = str()

@dp.message_handler(commands=['updatesheet'])
async def UpdateSheet(message: types.Message):
    if message.chat.id == message.from_user.id:
        Sheet = update_sheet()
        if str(message.from_user.id) in Sheet['access_id']:
            await bot.send_message(chat_id=message.chat.id, text='Данні оновлено. Щоб зробити запис натисніть  /start')
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.message_handler(commands=['counterrowsheet'])
async def Update_number_counter_Sheet(message: types.Message):
    if message.chat.id == message.from_user.id:
        if str(message.from_user.id) in Sheet['access_id']:
            writer.number = writer.update_number_writer()
            await bot.send_message(chat_id=message.chat.id, text='Лічильник рядків оновлено. Щоб зробити запис натисніть  /start')
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global Reply_message, Sheet
    m_id = Inline_Keyboard.func_message(message)[0]
    if message.chat.id == message.from_user.id:
        Sheet = checker()
        writer.number_writer()
        if str(message.from_user.id) in Sheet['access_id']:
            Reply_message[m_id] = dict()
            Reply_message[m_id]['text'] = ''

            DIP = [i for i in Sheet['dip']]
            Reply_message[m_id]['reported'] = Sheet['access_id'][str(m_id)]
            button = Inline_Keyboard.inline_c2_home(DIP)
            await bot.send_message(chat_id=message.chat.id, text='Оберіть команду:', reply_markup=button)
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass


@dp.callback_query_handler(lambda callback_query: True)
async def device_callback(call: types.CallbackQuery):
    global mq, Reply_message
    mq = ''
    button = types.InlineKeyboardMarkup(row_width=2)
    c_id = call.from_user.id
    try:
        Reply_message[c_id]['back'] = 'back'
        if call.data in 'back':
            await call.answer('')
            delete = ['team', 'dip', 'type', 'device', 'project', 'component', 'number_boards', 'amount', 'non_liquidity', 'repair']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            team = [i for i in Sheet['dip']]
            button = Inline_Keyboard.inline_c2_home(team)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Оберіть команду:',
                                                                                                                reply_markup=button)
        elif ((call.data in Sheet['dip']) and ('team' not in Reply_message[c_id])) or (call.data in 'back_dip'):
            await call.answer(call.data)
            delete = ['dip', 'type', 'device', 'project', 'component', 'number_boards', 'amount', 'non_liquidity', 'repair']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            if call.data in 'back_dip':
                pass
            else:
                Reply_message[c_id]['team'] = call.data
            DIP = [i for i in Sheet['dip'][Reply_message[c_id]['team']]]
            backer = 'back'
            button = Inline_Keyboard.inline_c2(DIP, backer, Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Оберіть монтажника:',
                                        reply_markup=button)
        elif call.data in Sheet['dip'][Reply_message[c_id]['team']]:
            await call.answer(call.data)
            delete = ['dip', 'type', 'device', 'project', 'component', 'number_boards', 'amount', 'non_liquidity', 'repair']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            Reply_message[c_id]['dip'] = call.data
            type = [i for i in Sheet['project_all']]
            backer = 'back_dip'
            button = Inline_Keyboard.inline_c2_nonBacker(type, backer)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Оберіть лінійку девайсів:',
                                reply_markup=button)
        elif call.data in Sheet['project_all']:
            await call.answer(call.data)
            delete = ['type', 'device', 'project', 'component', 'number_boards', 'amount', 'non_liquidity', 'repair']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            Reply_message[c_id]['type'] = call.data
            device = [i for i in Sheet['project_all'][Reply_message[c_id]['type']]]
            backer = 'dip'
            button = Inline_Keyboard.inline_c2(device, backer, Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Оберіть девайс:',
                                        reply_markup=button)
        elif call.data in Sheet['project_all'][Reply_message[c_id]['type']]:
            await call.answer(call.data)
            delete = ['device', 'project', 'component', 'number_boards', 'amount', 'non_liquidity', 'repair']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            Reply_message[c_id]['device'] = call.data
            project = [i for i in Sheet['project_all'][Reply_message[c_id]['type']][Reply_message[c_id]['device']]]
            backer = 'type'
            button = Inline_Keyboard.inline_c1(project, backer, Reply_message[c_id])
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Оберіть проект:',
                                        reply_markup=button)
        elif call.data in Sheet['project_all'][Reply_message[c_id]['type']][Reply_message[c_id]['device']]:
            await call.answer(call.data)
            delete = ['project', 'component', 'number_boards', 'amount', 'non_liquidity', 'repair']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            Reply_message[c_id]['project'] = call.data
            Reply_message[c_id]['number_boards'] = None
            button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data=Reply_message[c_id]['device']))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введіть кількість перевірених '
                                                                            'плат:', reply_markup=button)
        elif 'NOK_photo' in call.data:
            await call.answer('')
            delete = ['defect', 'component', 'amount', 'non_liquidity', 'repair']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            Reply_message[c_id]['stack_defects'] = ''
            Reply_message[c_id]['writer_stack'] = []
            button.add(types.InlineKeyboardButton(text='Без фото', callback_data='non_photo'),
                       types.InlineKeyboardButton(text='⬅️ Назад', callback_data='get_defect'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Зробіть фото '
                                                  'дефектів\nСумарна кількість фото не більше 10 на одне повідомлення', reply_markup=button)
        elif ('NOK_defect' in call.data) or ('non_photo' in call.data):
            await call.answer('')
            delete = ['amount', 'non_liquidity', 'repair']
            Reply_message[c_id][call.data] = call.data
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            defect = [i for i in Sheet['defects']]
            backer = 'NOK_photo' if Reply_message[c_id]['stack_defects'] in '' else 'back_post'
            button = Inline_Keyboard.inline_c2_nonBacker(defect, backer)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Оберіть дефект:',
                                        reply_markup=button)

        elif call.data in 'OK_non_defect':
            await call.answer('')
            button.add(types.InlineKeyboardButton(text='Так', callback_data='ve_sheet'),
                       types.InlineKeyboardButton(text='⬅️ Назад', callback_data='get_defect'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'Перевірте чи вірно сформовані '
                                                f'данні⬇️\n\n{assembler_message.assembling(Reply_message[c_id], Sheet)}', reply_markup=button)
        elif call.data in 've_sheet':
            await call.answer('')
            txt_non_defect = '✅Данні успішно записані в таблицю.\n\nЩоб зробити новий запис натисніть  /start'
            txt_defect = '✅Пост пересланий в чат QC THT\n✅Данні успішно записані в таблицю.\n\nЩоб зробити новий запис натисніть  /start'
            if ('med' in Reply_message[c_id]) and ('Не_монтажник' not in Reply_message[c_id]['dip']):
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=txt_defect)
                await bot.send_media_group(chat_id=Chat_test, media=Reply_message[c_id]['med'])
            elif ('non_photo' in Reply_message[c_id]) and ('Не_монтажник' not in Reply_message[c_id]['dip']):
                post = assembler_message.assembling_finished(Reply_message[c_id], Sheet)
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=txt_defect)
                await bot.send_message(chat_id=Chat_test, text=post)
            else:
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=txt_non_defect)
            if ('blocked' in Reply_message[c_id]) and (Reply_message[c_id]['blocked']):
                writer.writer_blocked(Reply_message[c_id], Sheet)
                Reply_message.pop(c_id)
            else:
                writer.writer(Reply_message[c_id], Sheet)
                Reply_message.pop(c_id)
        elif call.data in 'OK':
            await call.answer('')
            delete = ['defect', 'component', 'amount']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            if Reply_message[c_id]['med']:
                Reply_message[c_id]['text'] = assembler_message.assembling(Reply_message[c_id], Sheet)
                await bot.send_media_group(call.message.chat.id, media=Reply_message[c_id]['med'])
                await bot.send_message(call.message.chat.id, text='Переслати в чат?')
                writer.writer(Reply_message[c_id], Sheet)
                Reply_message.pop(c_id)
        elif call.data in Sheet['defects']:
            await call.answer(call.data)
            delete = ['component', 'amount']
            Reply_message[c_id]['defect'] = call.data
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            components = [i for i in Sheet['spec'][Reply_message[c_id]['project']]]
            backer = 'NOK_defect'
            button = Inline_Keyboard.inline_c2_nonBacker(components, backer)
            message = assembler_message.assembling_spec(Reply_message[c_id]['project'], Sheet=Sheet)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=message, reply_markup=button,
                                        parse_mode="HTML", disable_web_page_preview=True)
        elif ((call.data in Sheet['spec'][Reply_message[c_id]['project']]) and (call.data not in 'Інше')) or (call.data in 'back_amount'):
            await call.answer('')
            if call.data in 'back_amount':
                b = Reply_message[c_id]['stack_defects'].split('Дефект:')
                b = b[:-1]
                Reply_message[c_id]['stack_defects'] = 'Дефект:'.join(b)
                Reply_message[c_id]['writer_stack'] = Reply_message[c_id]['writer_stack'][:-1]
            else:
                Reply_message[c_id]['component'] = call.data
            Reply_message[c_id]['amount'] = None
            button.add(types.InlineKeyboardButton(text='⬅️ Hазад', callback_data=Reply_message[c_id]['defect']))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введіть кількість плат з'
                                                                                                            ' дефектом:', reply_markup=button)
        elif call.data in 'Інше':
            await call.answer('')
            Reply_message[c_id]['component'] = None
            button.add(types.InlineKeyboardButton(text='⬅️ Hазад', callback_data=Reply_message[c_id]['defect']))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введіть назву компонента:',
                                                                                                               reply_markup=button)
        elif call.data in 'non_liquidity':
            await call.answer('')
            Reply_message[c_id]['non_liquidity'] = None
            button.add(types.InlineKeyboardButton(text='⬅️ Hазад', callback_data='back_post'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введіть кількість неліквідних '
                                                                                                'плат:', reply_markup=button)
        elif call.data in 'repair':
            await call.answer('')
            Reply_message[c_id]['repair'] = None
            button.add(types.InlineKeyboardButton(text='⬅️ Hазад', callback_data='non_liquidity'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введіть кількість плат на '
                                                                    'ремонт:', reply_markup=button)
        elif (call.data in 'get_defect') or ('back_blocked' in call.data):
            await call.answer('')
            delete = ['blocked']
            Inline_Keyboard.deleter_key(delete, Reply_message[c_id])
            button.add(
                types.InlineKeyboardButton(text='Так', callback_data='NOK_photo'),
                types.InlineKeyboardButton(text='Ні', callback_data='OK_non_defect')
            )
            button.add(types.InlineKeyboardButton(text='Заблоковано ❌', callback_data='blocked'),
                types.InlineKeyboardButton(text='⬅️ Назад', callback_data=Reply_message[c_id]['project']))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Чи був виявлений дефект?',
                                        reply_markup=button)
        elif call.data in 'blocked':
            await call.answer('')
            Reply_message[c_id]['blocked'] = ''
            button.add(types.InlineKeyboardButton(text='Без фото', callback_data='non_photo'),
                       types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_blocked'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Зробіть фото '
                                                  'дефектів\nСумарна кількість фото не більше 10 на одне повідомлення', reply_markup=button)
        elif call.data in 'back_post':
            await call.answer('')
            button.add(
                types.InlineKeyboardButton(text='Додати дефект', callback_data='NOK_defect'),
                types.InlineKeyboardButton(text='Наступний крок ➡️', callback_data='non_liquidity')
            )
            button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_amount'))
            await bot.send_message(call.message.chat.id, text=f"{Reply_message[c_id]['stack_defects']}\n", reply_markup=button)
        elif 'back_photo_blocked' in call.data:
            await call.answer('')
            Reply_message[c_id]['blocked'] = ''
            button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='blocked'))
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Опишіть причину блокування '
                                                                                                    'партії:', reply_markup=button)
    except (KeyError, IndexError, AttributeError):
        pass


@dp.message_handler(content_types=['text'])
async def handle_files(message):
    if message.chat.id == message.from_user.id:
        if str(message.from_user.id) in Sheet['access_id']:
            global Reply_message, mq
            button = types.InlineKeyboardMarkup(row_width=2)
            try:
                m_id = Inline_Keyboard.func_message(message)[0]
                text_message = Inline_Keyboard.func_message(message)[1]
                if ('number_boards' in Reply_message[m_id]) and (not Reply_message[m_id]['number_boards']):
                    if message.text.isdigit():
                        if 0 <= int(message.text) <= 1500:
                            Reply_message[m_id]['number_boards'] = text_message
                            button.add(
                                types.InlineKeyboardButton(text='Так', callback_data='NOK_photo'),
                                types.InlineKeyboardButton(text='Ні', callback_data='OK_non_defect')
                            )
                            button.add(types.InlineKeyboardButton(text='Заблоковано ❌', callback_data='blocked'),
                                types.InlineKeyboardButton(text='⬅️ Назад', callback_data=Reply_message[m_id]['project']))
                            await bot.send_message(message.chat.id, text='Чи був виявлений дефект?', reply_markup=button)
                        else:
                            await bot.send_message(message.chat.id, text=assembler_message.input_validation_project)
                    else:
                        await bot.send_message(message.chat.id, text=assembler_message.input_validation_project)
                elif ('amount' in Reply_message[m_id]) and (not Reply_message[m_id]['amount']):
                    if message.text.isdigit():
                        if 0 < int(message.text) < 500:
                            Reply_message[m_id]['amount'] = text_message
                            button.add(
                                types.InlineKeyboardButton(text='Додати дефект', callback_data='NOK_defect'),
                                types.InlineKeyboardButton(text='Наступний крок ➡️', callback_data='non_liquidity')
                            )
                            button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='back_amount'))
                            Reply_message[m_id]['stack_defects'] += assembler_message.assembling_defect(Reply_message[m_id])
                            await bot.send_message(message.chat.id, text=f"{Reply_message[m_id]['stack_defects']}\n", reply_markup=button)
                    else:
                        await bot.send_message(message.chat.id, text=assembler_message.input_validation_defect)
                elif ('non_liquidity' in Reply_message[m_id]) and (not Reply_message[m_id]['non_liquidity']):
                    if message.text.isdigit():
                        if 0 <= int(message.text) <= 1500:
                            Reply_message[m_id]['non_liquidity'] = text_message
                            Reply_message[m_id]['repair'] = None
                            button.add(types.InlineKeyboardButton(text='⬅️ Назад', callback_data='non_liquidity'))
                            await bot.send_message(message.chat.id, text='Введіть кількість плат на ремонт', reply_markup=button)
                        else:
                            await bot.send_message(message.chat.id, text=assembler_message.input_validation_project)
                elif ('component' in Reply_message[m_id]) and (not Reply_message[m_id]['component']):
                    Reply_message[m_id]['component'] = text_message
                    Reply_message[m_id]['amount'] = None
                    button.add(types.InlineKeyboardButton(text='⬅️ Hазад', callback_data=Reply_message[m_id]['defect']))
                    await bot.send_message(message.chat.id, text='Введіть кількість плат з дефектом:', reply_markup=button)
                elif ('repair' in Reply_message[m_id]) and (not Reply_message[m_id]['repair']):
                    if message.text.isdigit():
                        if 0 <= int(message.text) <= 1500:
                            if 'non_photo' in Reply_message[m_id]:
                                Reply_message[m_id]['repair'] = text_message
                                post = assembler_message.assembling_finished(Reply_message[m_id], Sheet)
                                await bot.send_message(message.chat.id, post)
                            else:
                                Reply_message[m_id]['repair'] = text_message
                                post = assembler_message.assembling_finished(Reply_message[m_id], Sheet)
                                Reply_message[m_id]['med'] = []
                                for i in Reply_message[m_id]['photos']:
                                    if i != Reply_message[m_id]['photos'][-1]:
                                        Reply_message[m_id]['med'].append(types.InputMediaPhoto(media=i))
                                    else:
                                        Reply_message[m_id]['med'].append(types.InputMediaPhoto(media=i, caption=post))
                                for i in Reply_message[m_id]['videos']:
                                    if Reply_message[m_id]['photos']:
                                        Reply_message[m_id]['med'].append(types.InputMediaVideo(media=i))
                                    else:
                                        if i != Reply_message[m_id]['videos'][-1]:
                                            Reply_message[m_id]['med'].append(types.InputMediaVideo(media=i))
                                        else:
                                            Reply_message[m_id]['med'].append(types.InputMediaVideo(media=i, caption=post))
                                await bot.send_media_group(message.chat.id, media=Reply_message[m_id]['med'])
                            button.add(types.InlineKeyboardButton(text='Так', callback_data='ve_sheet'),
                                       types.InlineKeyboardButton(text='⬅️ Hазад', callback_data='repair'))
                            await bot.send_message(message.chat.id, text='Перевірте чи вірно сформовані данні', reply_markup=button)
                        else:
                            await bot.send_message(message.chat.id, text=assembler_message.input_validation_project)
                elif (('blocked' in Reply_message[m_id]) and (not Reply_message[m_id]['blocked'])) and (Reply_message[m_id]['photos']):
                    Reply_message[m_id]['blocked'] = text_message
                    post = assembler_message.assembling_blocked(Reply_message[m_id], Sheet)
                    Reply_message[m_id]['med'] = []
                    for i in Reply_message[m_id]['photos']:
                        if i != Reply_message[m_id]['photos'][-1]:
                            Reply_message[m_id]['med'].append(types.InputMediaPhoto(media=i))
                        else:
                            Reply_message[m_id]['med'].append(types.InputMediaPhoto(media=i, caption=post))
                    for i in Reply_message[m_id]['videos']:
                        if Reply_message[m_id]['photos']:
                            Reply_message[m_id]['med'].append(types.InputMediaVideo(media=i))
                        else:
                            if i != Reply_message[m_id]['videos'][-1]:
                                Reply_message[m_id]['med'].append(types.InputMediaVideo(media=i))
                            else:
                                Reply_message[m_id]['med'].append(types.InputMediaVideo(media=i, caption=post))
                    button.add(types.InlineKeyboardButton(text='Так', callback_data='ve_sheet'),
                        types.InlineKeyboardButton(text='⬅️ Hазад', callback_data='back_photo_blocked'))
                    await bot.send_media_group(message.chat.id, media=Reply_message[m_id]['med'])
                    await bot.send_message(message.chat.id, text='Перевірте чи вірно сформовані данні', reply_markup=button)
            except (KeyError, AttributeError, IndexError):
                pass
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')
    else:
        pass

@dp.message_handler(content_types=['video', 'photo'])
async def photo(message):
    global Reply_message, mq, Sheet
    m_id = Inline_Keyboard.func_message(message)[0]
    if message.chat.id == m_id:
        if str(message.chat.id) in Sheet['access_id']:
            if ('stack_defects' in Reply_message[m_id]) or ('blocked' in Reply_message[m_id]):
                if mq == '':
                    Reply_message[m_id]['photos'] = []
                    Reply_message[m_id]['videos'] = []
                    Reply_message[m_id]['med'] = []
                    Reply_message[m_id]['stack_defects'] = ''
                    Reply_message[m_id]['writer_stack'] = []
                delete = ['component', 'amount', 'defect']
                Inline_Keyboard.deleter_key(delete, Reply_message[m_id])
                defect = [i for i in Sheet['defects']]
                backer = 'NOK_photo'
                button = Inline_Keyboard.inline_c2_nonBacker(defect, backer)
                try:
                    Reply_message[message.chat.id]['photos'].append(message.photo[0].file_id)
                except (KeyError, IndexError):
                    pass
                try:
                    Reply_message[message.chat.id]['videos'].append(message.video.file_id)
                except AttributeError:
                    pass
                if mq == '':
                    mq = message.media_group_id
                    if 'blocked' in Reply_message[m_id]:
                        button = types.InlineKeyboardMarkup()
                        button.add(types.InlineKeyboardButton(text='⬅️ Hазад', callback_data='blocked'))
                        await bot.send_message(message.chat.id, text='Опишіть причину блокування партії:', reply_markup=button)
                    else:
                        await bot.send_message(message.chat.id, text='Оберіть дефект:', reply_markup=button)
        else:
            await bot.send_message(message.chat.id, 'Нажаль, у вас немає доступу до користування ботом!😢')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, timeout=False)