from aiogram.filters import CommandStart
from aiogram import types
from aiogram.fsm.context import FSMContext

from data.api_use import read_from_json
from handlers.users.buttons import button_for_lu, admins
from loader import dp
from states.login import LoginForm

token={}
for t in read_from_json('data/users.json'):
    token.update({'token':t['others']['access'],'role':t['others']['role'],'id':t['id']})
@dp.message(CommandStart())
async def start(msg:types.Message,state: FSMContext):
    if token['id']==msg.from_user.id:
        if token['role']=='student':
            await state.set_state()
            await msg.reply(f"Hi {msg.from_user.username}",reply_markup=button_for_lu)
        else:
            await msg.reply("Hi admin",reply_markup=admins)
    else:
        await state.set_state(LoginForm.username)
        await msg.reply(f'Hi {msg.from_user.username}\nyou should login first \nPlease enter your username')
