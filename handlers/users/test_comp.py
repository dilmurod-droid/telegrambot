import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State

from data.api_use import read_from_json, get_results
from handlers.users.buttons import button_for_lu
from loader import dp, bot

API_URL = "https://dilmurod0887.pythonanywhere.com/api/"
token={}
for t in read_from_json('data/users.json'):
    token.update({'token':t['others']['access']})
JWT_SECRET = token['token']

class TestStates(StatesGroup):
    select_test = State()
    answer_question = State()


# Fetch and display tests
@dp.message(F.text=='vocabulary test ✏️')
async def show_tests(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    token = JWT_SECRET  # Replace with actual JWT token retrieval
    headers = {'Authorization': f"Bearer {token}"}
    # Debugging: Print the API response
    response = requests.get(f"{API_URL}/tests/", headers=headers)
    print(response.text)  # Print the raw response

    try:
        tests = response.json()
    except ValueError as e:
        await message.answer("Failed to retrieve tests. Please try again.")
        print("Error parsing JSON:", e)
        return

    if isinstance(tests, list) and all(isinstance(test, dict) for test in tests):
        a=await message.answer("loading...", reply_markup=ReplyKeyboardRemove())
        builder = InlineKeyboardBuilder()
        for test in tests:
            builder.button(text=test['name'], callback_data=str(test['id']))
        await bot.delete_message(message.chat.id,a.message_id)
        await message.answer("Select a test:", reply_markup=builder.as_markup())
        await state.set_state(TestStates.select_test)
    else:
        await message.answer("Unexpected response format.")



@dp.callback_query(TestStates.select_test)
async def select_test(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    test_id = callback_query.data
    await state.update_data(test_id=test_id)

    # Fetch all questions
    state_data = await state.get_data()
    token = JWT_SECRET# Replace with actual JWT token retrieval
    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(f"{API_URL}questions/", headers=headers)
    print(f"Response for questions: {response.text}")  # Debugging: Print the raw response

    try:
        questions = response.json()
        if not questions:
            await callback_query.message.answer("No questions found.")
            return
    except ValueError as e:
        await callback_query.message.answer("Failed to retrieve questions. Please try again.")
        print("Error parsing JSON:", e)
        return

    # Filter questions based on selected test_id
    filtered_questions = [q for q in questions if q['test'] == int(test_id)]
    if not filtered_questions:
        await callback_query.message.answer("No questions found for the selected test.")
        return

    await state.update_data(questions=filtered_questions, current_question=0)
    user_id = 1
    data = {'user_id': user_id, 'test_id': test_id}
    requests.post(f"{API_URL}results/", headers=headers, json=data)

    await send_question(callback_query.message, state)


async def send_question(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    questions = state_data.get('questions', [])
    current_question = state_data.get('current_question', 0)

    if current_question < len(questions):
        question = questions[current_question]
        await message.answer(f"{question['text']}-You should write translate whis word uzb/ru")
        await state.update_data(current_question=current_question + 1)
        await state.set_state(TestStates.answer_question)
    else:
        token=JWT_SECRET
        results=get_results(token)
        for results in results:
            if results['failed']:
                await message.answer(f"You failed the test try again!😞\nYour scores:{results['score']}\nPassing score:80\nYour mistakes:{results['incorrect_answers']}",reply_markup=button_for_lu)
            else:
                await message.answer(
                    f"Congratulations, you passed the test.!🥳🤩\nYour scores:{results['score']}\nShould scores:80\nYour mistakes:{results['incorrect_answers']}",reply_markup=button_for_lu)
        await state.clear()


# Handle user answer and submit to user-answers endpoint
@dp.message(TestStates.answer_question)
async def handle_answer(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    user_id = 1  # Replace with actual user ID
    current_question_index = state_data['current_question'] - 1
    questions = state_data.get('questions', [])

    if current_question_index < len(questions):
        question_id = questions[current_question_index]['id']
        answer_text = message.text
        user_id=read_from_json('data/users.json')['others']['user_id']
        # POST the user answer to the server
        data = {
            'user': user_id,
            'question': question_id,
            'answer_text': answer_text
        }

        token = JWT_SECRET  # Replace with actual JWT token retrieval
        headers = {'Authorization': f'Bearer {token}'}

        response = requests.post(f"{API_URL}user-answers/", headers=headers, json=data)

        if response.status_code == 201:
            await message.answer("Your answer has been submitted.")
        else:
            await message.answer("There was an issue submitting your answer. Please try again.")
            print(response.text)
        await send_question(message, state)
    else:
        await message.answer("There was an issue. Please restart the test.")
        await state.clear()