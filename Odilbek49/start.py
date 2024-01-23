import asyncio
from os import getenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup;
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from dotenv import load_dotenv




load_dotenv();

class Registration(StatesGroup):
    typeYourName = State();

token = getenv('token')

bot = Bot(token);

dp = Dispatcher();

@dp.message(StateFilter(Registration.typeYourName))
async def nameHandler(message: Message, state: FSMContext):
    name = message.text;
    await state.set_data({'name': name});

@dp.message(Command('start'))
async def startHandler(message: Message, state: FSMContext) :
    # if message.chat.id 

        await message.answer("""бла бла бла - прикольная игра.

/new - запустить новую игру
/multiplayer - запустить игру с другом
/story - история игр
/profile - профиль
""");
    # else:
        # await state.set_state(RegisterState.requestName)
        # await message.answer('э, напиши свое имя !');

async def main():
    await dp.start_polling(bot);


if __name__ == "__main__":
    asyncio.run(main());