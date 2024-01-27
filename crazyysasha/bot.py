import asyncio
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from dotenv import load_dotenv

from crazyysasha.db import findUserByTelegramId




load_dotenv();

token = getenv('token')

bot = Bot(token);

dp = Dispatcher();


class RegisterState(StatesGroup):
    requestName = State();

@dp.message(Command('start'))
async def startHandler(message: Message, state: FSMContext) :
    if findUserByTelegramId(message.chat.id):

        await message.answer("""бла бла бла - прикольная игра.

/new - запустить новую игру
/multiplayer - запустить игру с другом
/story - история игр
/profile - профиль
""");
    else:
        await state.set_state(RegisterState.requestName)
        await message.answer('э, напиши свое имя !');

async def main():
    await dp.start_polling(bot);


if __name__ == "__main__":
    asyncio.run(main());