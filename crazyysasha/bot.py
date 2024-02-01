import asyncio
from os import getenv
from random import randint
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

from db import createUser, findUserByTelegramId




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


@dp.message(StateFilter(RegisterState.requestName))
async def registerHandler(message: Message, state: FSMContext):
    createUser(name=message.text, telegram_id= message.from_user.id);
    await message.answer('спасибо!')
    await state.set_state();


class GameState(StatesGroup):
    loop=State();

@dp.message(Command('new'))
async def startGame(message: Message, state: FSMContext):
    await message.answer('игра началась, удачи!', 
        reply_markup=ReplyKeyboardMarkup(
            resize_keyboard= True,
            keyboard=[
                [
                    KeyboardButton(text="Камень"),
                    KeyboardButton(text="Ножницы"),
                    KeyboardButton(text="Бумага"),
                ]
            ]
        )
    );
    await state.set_state(GameState.loop);


@dp.message(StateFilter(GameState.loop))
async def gameLoop(message: Message, state: FSMContext):
    botTurn = randint(0,2)
    # 0:0 tie
    # 0:1 lose
    # 0:2 win 
    # 1:0 win
    # 1:1 tie
    # 1:2 lose
    # 2:0 lose
    # 2:1 win
    # 2:2 tie

    table = {
        '0:0': 'tie',
        '0:1': 'lose',
        '0:2': 'win',
        '1:0': 'win',
        '1:1': 'tie',
        '1:2': 'lose',
        '2:0': 'lose',
        '2:1': 'win',
        '2:2': 'tie',
    }
    turns = ["Камень", "Ножницы", "Бумага"]
    
    await message.answer(f'{table[f"{botTurn}" + ":" + f"{turns.index(message.text)}"]} {turns[botTurn]}')

async def main():
    await dp.start_polling(bot);


if __name__ == "__main__":
    asyncio.run(main());