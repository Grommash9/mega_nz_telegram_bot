import asyncio
import datetime
import logging
import os
import threading
import time

import aiogram
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from aiogram.utils.exceptions import BotBlocked, MessageIsTooLong
import config
import db_api

import data_base_sender
import keyboards
import mega_nz_api

bot = Bot(token=config.bot_token)
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, storage=storage, loop=loop)


class Form(StatesGroup):
    new_file_name = State()
    current_file_name = State()
    manager_id = State()
    manager_action = State()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    db_api.add_user(id=message.from_user.id, username=message.from_user.username, full_name=message.from_user.full_name,
                    registration_date=str(message.date), language=message.from_user.language_code)
    await bot.send_message(chat_id=message.from_user.id, text='Hi',
                           reply_markup=keyboards.default_reply_keyboard(user_id=message.from_user.id))


@dp.message_handler(commands=['id'])
async def process_id_command(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=str(message.from_user.id))


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    if db_api.get_user(id=message.from_user.id)[5] == 1 or message.from_user.id == config.owner_id:
        current_state = await state.get_state()
        if current_state is None:
            return

        logging.info('Cancelling state %r', current_state)

        await state.finish()
        await bot.send_message(chat_id=message.from_user.id, text='You are canceled the operation')
    else:
        await bot.send_message(chat_id=message.from_user.id, text='You have no permission to run this command')


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('del'))
async def delete(callback_query: types.CallbackQuery):
    callback_data = callback_query.data.split('_')
    file = db_api.get_user_files_data(id=callback_data[1])
    if len(file) > 0:

        db_api.delete_files_data(id=callback_data[1])
        await bot.send_message(chat_id=callback_query.from_user.id, text=f'File {file[0][1]} has been deleted')
        await bot.answer_callback_query(callback_query_id=callback_query.id)
    else:
        await bot.send_message(chat_id=callback_query.from_user.id,
                               text=f'Cant find this file')
        await bot.answer_callback_query(callback_query_id=callback_query.id)


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def file_handle(message: types.Document, state: FSMContext):
    files_names = [0]
    for files in os.listdir(config.files_path):
        try:
            files_names.append(int(files.split('.zip')[0]))
        except ValueError:
            pass
    new_file_name = str(max(files_names) + 1)
    async with state.proxy() as data:
        data['current_file_name'] = f"{new_file_name}.zip"

    file = await bot.get_file(file_id=message.document.file_id)
    await bot.download_file(file_path=file.file_path, destination=f"{config.files_path}/{new_file_name}.zip")
    await Form.new_file_name.set()
    await message.answer(text=f'Use /cancel to cancel\n\nPlease enter the file name:')


@dp.message_handler(state=Form.new_file_name)
async def new_file_name_getter(message: types.Message, state: FSMContext):
    if db_api.get_user(id=message.from_user.id)[5] == 1 or message.from_user.id == config.owner_id:
        async with state.proxy() as data:
            data['new_file_name'] = message.text
        local_file_name = data['current_file_name']
        x = threading.Thread(target=mega_nz_api.file_upload, args=(local_file_name, data['new_file_name'], message.from_user.id,))
        x.start()
        await state.finish()
        await bot.send_message(chat_id=message.from_user.id, text='Download initialized')
    else:
        await bot.send_message(chat_id=message.from_user.id, text='You have no permission to run this command')


@dp.message_handler(aiogram.dispatcher.filters.Text(equals='My list'))
async def my_list_callback(message: types.Message):
    if db_api.get_user(id=message.from_user.id)[5] == 1 or message.from_user.id == config.owner_id:
        files_list = db_api.get_user_files_data(owner=message.from_user.id)
        if len(files_list) > 0:
            files_str_data = ''
            for files in files_list:
                files_str_data += f"{files[1]}  -  {files[2]}\n\n"
            await bot.send_message(chat_id=message.from_user.id, text='You files:\n\n'
                                                                      f'{files_str_data}')
        else:
            await bot.send_message(chat_id=message.from_user.id, text='You have no files now')
    else:
        await bot.send_message(chat_id=message.from_user.id, text='You have no permission to run this command')


@dp.message_handler(aiogram.dispatcher.filters.Text(equals='Add manager'))
async def my_list_callback(message: types.Message, state: FSMContext):
    if message.from_user.id == config.owner_id:
        async with state.proxy() as data:
            data['manager_action'] = 'add'
        await Form.manager_id.set()
        await bot.send_message(chat_id=message.from_user.id, text='Use /cancel to cancel\n\nPlease enter user id')


@dp.message_handler(aiogram.dispatcher.filters.Text(equals='Remove manager'))
async def my_list_callback(message: types.Message, state: FSMContext):
    if message.from_user.id == config.owner_id:
        async with state.proxy() as data:
            data['manager_action'] = 'del'
        await Form.manager_id.set()
        await bot.send_message(chat_id=message.from_user.id, text='Use /cancel to cancel\n\nPlease enter user id')


@dp.message_handler(state=Form.manager_id)
async def new_file_name_getter(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['manager_id'] = message.text
    await state.finish()
    user = db_api.get_user(id=data['manager_id'])
    if user != None:
        if data['manager_action'] == 'add':
            db_api.update_user(id=data['manager_id'], is_manager=1)
            await bot.send_message(chat_id=message.from_user.id, text=f"added to managers:\n\n"
                                                                      f"{user[0]} - {user[1]} - {user[2]}")
            await bot.send_message(chat_id=user[0], text='You are manager now')
        elif data['manager_action'] == 'del':
            db_api.update_user(id=data['manager_id'], is_manager=0)
            await bot.send_message(chat_id=message.from_user.id, text=f"removed from managers:\n\n"
                                                                      f"{user[0]} - {user[1]} - {user[2]}")
            await bot.send_message(chat_id=user[0], text='You are not manager now')
    else:
        await bot.send_message(chat_id=message.from_user.id, text=f"Cant find user with id {data['manager_id']}")


@dp.message_handler(aiogram.dispatcher.filters.Text(equals='Manager list'))
async def my_list_callback(message: types.Message):
    if message.from_user.id == config.owner_id:
        manager_list = db_api.get_users(is_manager=1)
        if len(manager_list) > 0:
            manager_str = ''
            for manager in manager_list:
                manager_str += f"{manager[0]} - {manager[1]} - {manager[2]}\n\n"
            await bot.send_message(chat_id=message.from_user.id, text='Managers list:\n\n'
                                                                      f'{manager_str}')
        else:
            await bot.send_message(chat_id=message.from_user.id, text='There are no any managers now')


@dp.message_handler()
async def any_message_answer(message: types.Message):
    if db_api.get_user(id=message.from_user.id)[5] == 1 or message.from_user.id == config.owner_id:
        files_list = db_api.get_user_files_data(owner=message.from_user.id)
        if len(files_list) > 0:
            for files in files_list:
                if files[1] == message.text:
                    await bot.send_message(chat_id=message.from_user.id, text='Hello Sir\n\n'
                                                                              'here is Your Link\n\n'
                                                                              f'{files[2]}', reply_markup=keyboards.delete_button(file_id=files[0]))
                    await bot.send_message(chat_id=message.from_user.id, text='System message for return the main keyboard',reply_markup=keyboards.default_reply_keyboard(user_id=message.from_user.id))
                    break
            else:
                await bot.send_message(chat_id=message.from_user.id, text="Can't find this file,"
                                                                          " try to check name in file list")
        else:
            await bot.send_message(chat_id=message.from_user.id, text='You cant search files now, please upload first')
    else:
        await bot.send_message(chat_id=message.from_user.id, text='You have no permission to search files')

if __name__ == '__main__':
    dp.loop.create_task(data_base_sender.data_base_sender())
    executor.start_polling(dp)


