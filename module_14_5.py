from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions14_5 import *


def populate_products():
    add_product("Product1", "Описание 1", 100)
    add_product("Product2", "Описание 2", 200)
    add_product("Product3", "Описание 3", 300)
    add_product("Product4", "Описание 4", 400)
    print("Таблица Products успешно заполнена!")


initiate_product_db()
initiate_users_db()
populate_products()

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
button4 = KeyboardButton(text='Регистрация')
kb.add(button, button2, button3, button4)

catalog_kb = InlineKeyboardMarkup()


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Выберите опцию', reply_markup=kb)


@dp.message_handler(text="Купить")
async def get_buying_list(message: types.Message):
    products = get_all_products()
    if not products:
        await message.answer("Нет доступных продуктов.")
        return

    for product in products:
        product_id, title, description, price = product
        product_text = f'Название: {title} | Описание: {description} | Цена: {price}'
        await message.answer(product_text)
        await message.answer_photo(photo=open(f'{product_id}.jpeg', 'rb'))
        catalog_kb.add(InlineKeyboardButton(text=title, callback_data=f'product_{product_id}'))

    await message.answer('Выберите продукт для покупки:', reply_markup=catalog_kb)


@dp.callback_query_handler(lambda call: call.data.startswith('product_'))
async def send_confirm_message(call: types.CallbackQuery):
    product_id = call.data.split('_')[1]
    await call.answer('Вы выбрали продукт для покупки. Подтвердите покупку?', show_alert=True)
    confirm_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text='Подтвердить', callback_data=f'confirm_{product_id}')],
            [InlineKeyboardButton(text='Отмена', callback_data='cancel_buying')]
        ]
    )
    await call.message.answer('Подтвердите покупку:', reply_markup=confirm_kb)


@dp.callback_query_handler(lambda call: call.data.startswith('confirm_'))
async def confirm_buying(call: types.CallbackQuery):
    await call.answer('Вы успешно приобрели продукт!')


@dp.callback_query_handler(text="cancel_buying")
async def cancel_buying(call: types.CallbackQuery):
    await call.answer('Покупка отменена.')


@dp.message_handler(text="Регистрация")
async def sing_up(message: types.Message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    username = message.text
    if is_included(username):
        await message.answer("Пользователь с таким именем уже существует, введите другое имя:")
    else:
        await state.update_data(username=username)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    email = message.text
    await state.update_data(email=email)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    age = message.text
    await state.update_data(age=age)
    data = await state.get_data()
    username = data['username']
    email = data['email']
    age = int(data['age'])
    add_user(username, email, age)
    await message.answer("Регистрация завершена!")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
