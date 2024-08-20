from aiogram import F,types

from data.api_use import get_profile,read_from_json
from loader import dp
token={}
for t in read_from_json('data/users.json'):
    token.update({'token':t['others']['access'],'role':t['others']['role'],'id':t['id']})

@dp.message(F.text=="My Profile 👤")
async def profile(msg:types.Message):
    data=get_profile(token['token'])
    for data in data:
        await msg.answer(f"ID:<b>{data['id']}</b>\nusername:<b>{data['username']}</b>")