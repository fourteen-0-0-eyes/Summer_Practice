from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from handlers.game import GameState

from markup import start_markup


async def cmd_start(message: types.Message, state: FSMContext):
    state_current = await state.get_state()
    if state_current == GameState.in_process.state:
        await message.answer(
            "Игра уже началась",
            reply_markup=None
        )
    else:
        await message.answer(
            f"Привет, {message.chat.first_name}, я хочу сыграть с тобой в одну игру :)",
            reply_markup=start_markup
        )


async def cmd_help(message: types.Message, state: FSMContext):
    state_current = await state.get_state()
    if state_current == GameState.in_process.state:
        await message.answer(
            "Чтобы завершить игру, напиши /cancel",
            reply_markup=types.ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "Чтобы начать игру, напиши /start",
            reply_markup=types.ReplyKeyboardRemove()
        )


async def cmd_exit(message: types.Message, state: FSMContext):
    state_current = await state.get_state()
    if state_current == GameState.in_process.state:
        await state.finish()
        await message.answer("Игра завершена")
    else:
        await message.answer("Ты не в игре")


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_help, commands="help", state="*")
    dp.register_message_handler(cmd_exit, commands="cancel", state="*")
