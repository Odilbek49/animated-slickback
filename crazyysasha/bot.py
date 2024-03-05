import asyncio
from os import getenv
from random import randint
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage

from db import createGameHistory, createUser, findUserByTelegramId, getAllUserResults




load_dotenv();

token = getenv('token')

bot = Bot(token);

dp = Dispatcher();


class RegisterState(StatesGroup):
    requestName = State();

@dp.message(Command('start'))
async def startHandler(message: Message, state: FSMContext, command: CommandObject) :
    userId = command.args;
    if userId:
        await state.set_data({"players" : [userId, message.chat.id]})
        await state.set_state(GameState.loop);
        GameState.loop.state
        state2 = FSMContext(storage=MemoryStorage(), key= StorageKey(bot_id= message.bot.id, user_id= message.from_user.id, chat_id= message.chat.id));
        await state2.set_state(GameState.loop);
        await state2.set_data({"players": [userId, message.chat.id]})
        await message.answer("igra nachalas");
        await message.bot.send_message(chat_id= userId, text="polzovatel podklyuchilsya igra nachalas'");
    elif findUserByTelegramId(message.chat.id):

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
    winOrLose  = table[f'{botTurn}:{turns.index(message.text)}'];
    createGameHistory({'win': message.chat.id, 'tie': 'tie', 'lose': 'bot'}[winOrLose], ['bot', message.chat.id]);
    await message.answer(f'{table[f"{botTurn}" + ":" + f"{turns.index(message.text)}"]} {turns[botTurn]}')


@dp.message(Command('multiplayer'))
async def multiplayerStart (message: Message, state: FSMContext):
    userId = message.chat.id;
    await message.answer(f"привет, игра создалась приглоси 2 го игрока <a href=\"https://t.me/cyberhubsupportbot?start={userId}\"> /start</a>", parse_mode= "html");

@dp.message(Command('story'))
async def handleStory(message: Message):
    s = '';
    games = getAllUserResults(message.chat.id);

    for  game in games:
        s += f'{game[0]}. {game[1]} - {game[2]} \n' 
    await message.answer(s)

async def main():
    await dp.start_polling(bot);


if __name__ == "__main__":
    asyncio.run(main());