import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from client import get_access_envs
from config import TOKEN, YANDEX_ORG_API

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL = "https://search-maps.yandex.ru/v1"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class AIQuestion(StatesGroup):
    waiting_for_question = State()


## добавить обработку /start

### добавить обработку ответа без команд

@dp.message(Command("ai"))
async def ai_handler(message: Message, state: FSMContext):
    await message.answer("✍ Напиши место, для которого нужно проверить доступность.")
    await state.set_state(AIQuestion.waiting_for_question)


@dp.message(AIQuestion.waiting_for_question)
async def process_ai_question(message: Message, state: FSMContext):
    place_name = message.text.strip()
    if not place_name:
        await message.answer("❌ Пожалуйста, укажи название места.")
        return
    else:
        text_list = await get_access_envs(url=URL, api_key=YANDEX_ORG_API, place=place_name)
        response = "<b>Вот информация по доступной среде:</b>"
        for acces_env in text_list:
            response = response + f"• {acces_env}" + "\n\n"

        await message.answer(text=response, parse_mode="HTML")

    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
