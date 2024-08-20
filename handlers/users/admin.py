import time

from aiogram import F,types

from data.api_use import read_from_json, get_test_and_user_details
from loader import dp, bot

token={}
for t in read_from_json('data/users.json'):
    token.update({'token':t['others']['access'],'role':t['others']['role']})
@dp.message(F.text=="Users👥")
async def get_users(msg:types.Message):
    if token['role'] == 'mentor':
        a=await msg.answer('loading...')
        data=get_test_and_user_details()
        time.sleep(4)
        await bot.delete_message(msg.chat.id, a.message_id)
        for data in data:
            await msg.reply(f"Username:<b>{data['Username']}</b>\nSolved tests:<b>{data['Test_Name']}</b>\nFailed:<b>{data['Failed']}</b>")