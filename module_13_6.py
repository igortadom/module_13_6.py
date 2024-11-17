from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = 'api'
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb_1 = InlineKeyboardMarkup(resize_keyboard=True)
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_1.row(button1, button2)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_1 = KeyboardButton(text='Рассчитать')
button_2 = KeyboardButton(text='Информация')
kb.row(button_1, button_2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands = ['start'])
async def start_(message):
    await message.answer(text='Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)



@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer(text='Выберите опцию:', reply_markup=kb_1)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('(10 x вес(кг)) +(6,25 x рост(см)) – (5 x возраст(г) + 5')

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(text = ['Информация'])
async def inform(message):
    await message.answer('Этот бот поможет рассчитать ежедневные калории.')

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5)
    await message.answer(f"Ваша норма калорий: {result} ккал в сутки.")
    await state.finish()

@dp.message_handler()
async def start_any(message):
    await message.answer('Введите команду /start чтобы начать общение')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)










