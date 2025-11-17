import logging
import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

TOKEN = os.getenv('TOKEN')

#состояние
class MyStates(StatesGroup):
    waiting_for_text = State()

#бот
bot = Bot(token=TOKEN)

#диспетчер
dp = Dispatcher()

#логирование
logging.basicConfig(level=logging.INFO, filename = 'mylog.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    logging.info(f'{message.from_user.username}: запустил бота')
    await message.answer(f'''Приветствую, {message.from_user.username}!
Вы можете ввести команду /fio, написать свое ФИО и получите ФИО на латинице :)''') 

@dp.message(Command('fio'))
async def cmd_fio(message: types.Message, state: FSMContext):
    await message.answer('Введите ФИО, которое хотите обработать')
    await state.set_state(MyStates.waiting_for_text)

@dp.message(MyStates.waiting_for_text)
async def trans_fio(message: types.Message, state: FSMContext):
    user_text = message.text
    translit_dict = {
    'А': 'A', 'Б': 'B' ,'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E' ,'Ё': 'E', 
    'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M',
    'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 
    'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 
    'Ы': 'Y', 'Ъ': 'IE', 'Э': 'E', 'Ю': 'IU', 'Я': 'IA'
}
    
    res = ''
    for char in user_text.upper():
        if char == 'Ь':
            continue
        res += translit_dict.get(char, char)

    logging.info(f'Пользователь {message.from_user.username} написал ФИО: {user_text}')    
    await message.answer(res)
    await state.clear()

@dp.message()
async def echo_message(message: types.Message):
    logging.info(f'Получено сообщение от {message.from_user.id}: {message.text}')
    #await message.answer('Я получил твое сообщение!')

async def main():
    logging.info('Бот запускается...')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())