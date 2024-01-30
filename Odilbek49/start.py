import asyncio
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton;
from dotenv import load_dotenv

from db import findUserByTelegramId, createUser




load_dotenv();

token = getenv('token')

bot = Bot(token);

dp = Dispatcher();

markup = ReplyKeyboardMarkup(
    keyboard=[[
        KeyboardButton(text="Камень"),
        KeyboardButton(text="Ножница"),
        KeyboardButton(text="Бумага"),
    ]]
)

class RegisterState(StatesGroup):
   requestName = State();

@dp.message(Command('start'))
async def startHandler(message: Message, state: FSMContext) :
    if findUserByTelegramId (message.chat.id):
     await message.answer("""бла бла бла - прикольная игра.

/new - запустить новую игру
/multiplayer - запустить игру с другом
/story - история игр
/profile - профиль
""");
    else:
        await state.set_state(RegisterState.requestName)
        await message.answer('Напишите свое имя для регистратции');
        

@dp.message(StateFilter(RegisterState.requestName))
async def handleName(message: Message, state: FSMContext):
#    print(message.text);
    # create user into db
    createUser(message.text, message.chat.id);
    await message.answer("спасибо за регистрацию")
    await state.set_state();
    await message.answer("""бла бла бла - прикольная игра.

/new - запустить новую игру
/multiplayer - запустить игру с другом
/story - история игр
/profile - профиль
""");

@dp.message(Command('new'))
async def newHendler(message: Message, state: FSMContext):
   await message.answer('Игра начилась, Удачи!', reply_markup= markup);


async def main():
    await dp.start_polling(bot);


if __name__ == "__main__":
    asyncio.run(main());