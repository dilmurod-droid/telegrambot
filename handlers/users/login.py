from aiogram import types
from aiogram.fsm.context import FSMContext

from data.api_use import login, write_to_json, read_from_json
from handlers.users.buttons import button_for_lu
from loader import dp, storage
from states.login import LoginForm


@dp.message(LoginForm.username)
async def send_hello(msg: types.Message,state: FSMContext):
    await msg.delete()
    await msg.answer("Please enter your password")
    await state.update_data({'username':msg.text})
    await state.set_state(LoginForm.password)

@dp.message(LoginForm.password)
async def get_password(msg:types.Message,state:FSMContext):
    await msg.delete()
    data=await state.update_data({'password':msg.text})
    login_data=login(f"{data.get('username')}",f"{data.get('password')}")
    login_data_2 = {'id': msg.from_user.id, 'others': login_data}
    if  'non_field_errors' in login_data:
        await msg.answer("Login field please login again\nplease enter your username")
        await state.set_state(LoginForm.username)
    else:
        write_to_json('data/users.json',login_data_2)
        await msg.answer('login was successful\n /start ')
