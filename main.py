
import psycopg2
from config import host, user, password, db_name
import time
import utils
import requests
from aiogram.types import InputMediaPhoto
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram import executor
import time
from datetime import datetime 
import requests
import json
import utils
from decimal import Decimal



admin = 5359516739
admin2 = 5655897574
variable = utils.Variable()
API_TOKEN = "6530283151:AAGIjz4ckeRUTa9znRu1aSVrlrDVEn2ZkDc"
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
  global mess
  k = types.InlineKeyboardMarkup()
  k1 = types.InlineKeyboardButton(text="WEB APP", web_app=types.WebAppInfo(url="https://main--dancing-cheesecake-968061.netlify.app"))
  k.add(k1)
  await bot.send_message(message.chat.id, text= "Приложение тут", reply_markup=k)
  variable.set_action(message.chat.id, 0)


@dp.message_handler(commands=['admin'])
async def send_welcome(message: types.Message):
  if message.chat.id == admin or message.chat.id == admin2:
    kb_ad = types.InlineKeyboardMarkup(row_width=2)
    k1 = types.InlineKeyboardButton(text="КУРС",callback_data="curs")
    k2 = types.InlineKeyboardButton(text="ТРЕК",callback_data="trek")   
    kb_ad.add(k1,k2) 
    await bot.send_message(message.chat.id, text="Вы попали в меню администратора\nИсползуйте кнопки ниже",reply_markup=kb_ad)
    variable.set_action(message.chat.id, 0)

@dp.callback_query_handler(lambda call: True)
async def print_all_commands(call: types.CallbackQuery):
  if call.data == "curs":
    
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name    
    )
    connection.autocommit = True

    # #     connection.commit()
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT course FROM yuan"""
        )    
        qe = (cursor.fetchone()[0])
        
    kb_change_curs = types.InlineKeyboardMarkup(row_width=1)
    k1 = types.InlineKeyboardButton(text="СМЕНА",callback_data="cc")
    k2 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_curs.add(k1,k2)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.mess.message_id,text=f"Актуальный курс - {qe}",reply_markup=kb_change_curs)
    variable.set_action(call.message.chat.id, 0)

  if call.data == "trek":
    kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
    k1 = types.InlineKeyboardButton(text="ДОБАВИТЬ",callback_data="at") 
    k2 = types.InlineKeyboardButton(text="ПОИСК",callback_data="ft") 
    k3 = types.InlineKeyboardButton(text="УДАЛИТЬ",callback_data="dt") 
    k4 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_trak.add(k1,k2,k3,k4)
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text= "Меню Треккинга заказов",reply_markup=kb_change_trak)
  if call.data == "back":
    kb_ad = types.InlineKeyboardMarkup(row_width=2)
    k1 = types.InlineKeyboardButton(text="КУРС",callback_data="curs")
    k2 = types.InlineKeyboardButton(text="ТРЕК",callback_data="trek")   
    kb_ad.add(k1,k2) 
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,text="Вы попали в меню администратора\nИсползуйте кнопки ниже",reply_markup=kb_ad)
    variable.set_action(call.message.chat.id, 0)

  if call.data == "dt":

    kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
    k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_trak.add(k3)
    await bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text= "Введите трек номер заказа для удаления трек номера",reply_markup=kb_change_trak)
    variable.set_action(call.message.chat.id, 5)
  if call.data == "cc":

    kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
    k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_trak.add(k3)
    await bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text= "Введите новый курс",reply_markup=kb_change_trak)
    variable.set_action(call.message.chat.id, 1) 
  if call.data == "at":

    kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
    k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_trak.add(k3)
    await bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text=  "Введите новый трек номер и его статус через пробел\n\nПример (AE14713894 1)\n\n1. Выкуплен, в пути склад\n2. Принят на складе, оформляется\n3. Заказ в пути\n4. Сортируется в Москве be\n5. Передан в СДЭК\n6. Получен клиентом",reply_markup=kb_change_trak)
    variable.set_action(call.message.chat.id, 2)  
  if call.data == "ft":
    
    kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
    k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_trak.add(k3)
    await bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text= "Введите трек номер заказа для смены статуса",reply_markup=kb_change_trak)
    variable.set_action(call.message.chat.id, 3)
@dp.message_handler(lambda message: True, content_types=['text'])
async def handle_text(message: types.Message):
  global treknom
  text = message.text
  action = int(variable.get_action(message.chat.id))


  if action == 1:
    curs = message.text
    connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name    
    )
    connection.autocommit = True
    try:
      with connection.cursor() as cursor:
          cursor.execute(
              f"""UPDATE yuan SET course = {message.text}"""
          )

      #     connection.commit()
      with connection.cursor() as cursor:
          cursor.execute(
              """SELECT course FROM yuan"""
          )    
          print(cursor.fetchone()[0])
          
          kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
          k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
          kb_change_trak.add(k3)
          await bot.send_message(message.chat.id, f"Актуальный курс - {message.text}",reply_markup=kb_change_trak)
          variable.set_action(message.chat.id, 0)
    except:

      kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
      k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
      kb_change_trak.add(k3)
      await bot.send_message(message.chat.id, "Введите новый курс\nПример 13.5",reply_markup=kb_change_trak)
      variable.set_action(message.chat.id, 1)
  
  if action == 2:
    try:
      lines = message.text.split("\n")
      for line in lines:
        
        trak = line.split(" ")[0]
        status = line.split(" ")[1]
        print(trak,status)
        connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name    
        )
        connection.autocommit = True
        try:
          with connection.cursor() as cursor:
              cursor.execute(
                  f"""SELECT status FROM orders WHERE track = '{trak}'"""
              )
              a = cursor.fetchone()[0]
              
              with connection.cursor() as cursor:
                cursor.execute(
                    f"""UPDATE orders SET status = {status} WHERE track = '{trak}'"""
                )
        except:
          with connection.cursor() as cursor:
              cursor.execute( 
                f"""INSERT INTO orders (track,status) VALUES ('{trak}',{status})"""
              )



        
      kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
      k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
      kb_change_trak.add(k3)
      await bot.send_message(message.chat.id, "Успешно добавлен трек номер",reply_markup=kb_change_trak)
      variable.set_action(message.chat.id, 0)

    except:
      
      kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
      k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
      kb_change_trak.add(k3)
      await bot.send_message(message.chat.id, "Введите новый трек номер и его статус через пробел\n\nПример (AE14713894 1)\n\n1. Выкуплен, в пути склад\n2. Принят на складе, оформляется\n3. Заказ в пути\n4. Сортируется в Москве be\n5. Передан в СДЭК\n6. Получен клиентом",reply_markup=kb_change_trak)
      variable.set_action(message.chat.id, 2)
  if action == 3:
    try:
      # поиск по номеру заказа 
      connection = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name    
      )
      connection.autocommit = True
      trak = message.text
      treknom = message.text
      with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT status FROM orders WHERE track = '{trak}';"""
        )
        
        a = cursor.fetchone()
        print(a)
        kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
        k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
        kb_change_trak.add(k3)

        await bot.send_message(message.chat.id, f"трек номер {trak}\nСтатус - {a[0]}\nВведите новый статус заказа ",reply_markup=kb_change_trak)
        variable.set_action(message.chat.id, 4)
    except:
      
      kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
      k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
      kb_change_trak.add(k3)
      await bot.send_message(message.chat.id, "Введите трек номер заказа для смены статуса",reply_markup=kb_change_trak)
      variable.set_action(message.chat.id, 3)
  if action == 4:
    stat = message.text
    connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name    
    )
    connection.autocommit = True
    
    with connection.cursor() as cursor:
        cursor.execute(
            f"""UPDATE orders SET status = {message.text} WHERE track = '{treknom}'"""
        )
    
    kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
    k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
    kb_change_trak.add(k3)
    await bot.send_message(message.chat.id, "Успешно добавлен трек номер",reply_markup=kb_change_trak)
    variable.set_action(message.chat.id, 0)
  if action == 5:
    trak = message.text
    treknom = message.text
    try:
      # поиск по номеру заказа 
      connection = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name    
      )
      connection.autocommit = True
      
      with connection.cursor() as cursor:
        cursor.execute(
            f"""SELECT status FROM orders WHERE track = '{trak}';"""
        )
        a = cursor.fetchone()[0]
        cursor.execute(
            f"""DELETE FROM orders WHERE track = '{trak}';"""
        ) 
        kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
        k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
        kb_change_trak.add(k3)
        
        await bot.send_message(message.chat.id, f"УСПЕШНО УДАЛЕНО",reply_markup=kb_change_trak)
        variable.set_action(message.chat.id, 0)
    except:
      
      kb_change_trak = types.InlineKeyboardMarkup(row_width=1)
      k3 = types.InlineKeyboardButton(text="НАЗАД",callback_data="back") 
      kb_change_trak.add(k3)
      await bot.send_message(message.chat.id, "Введите трек номер заказа для удаления трек номера",reply_markup=kb_change_trak)
      variable.set_action(message.chat.id, 5)

from aiogram import executor
executor.start_polling(dp, skip_updates=True) 



