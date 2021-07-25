from random import randint

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from markup import start_markup

user_data = {}
with open("words.txt", "r", encoding="utf-8") as file_r:
    words = file_r.read().split('\n')


class GameState(StatesGroup):
    in_process = State()


async def game_initialize(callback_query: types.CallbackQuery, state: FSMContext):
    state_current = await state.get_state()
    if state_current == GameState.in_process.state:
        await callback_query.message.edit_text(
            "Игра уже началась",
            reply_markup=None
        )
    else:
        await callback_query.message.delete()
        word = words[randint(1, len(words) - 1)].lower()
        hidden_word = ['_' for _ in word]
        mistakes = 0
        user_data[callback_query.message.chat.id] = {
            "word": word,
            "hidden_word": hidden_word,
            "mistakes": mistakes
        }
        await callback_query.message.answer(
            f"Я загадал слово с количеством букв: {len(hidden_word)}\n"
            f"Отгадай его за 10 попыток\n\n" +
            " ".join(hidden_word)
        )
        await GameState.in_process.set()


async def game_letter_chosen(message: types.Message, state: FSMContext):
    answer = ""
    user = user_data[message.chat.id]
    input_letter = message.text.lower()
    if user["mistakes"] < 10 and '_' in user["hidden_word"]:
        if input_letter.isalpha() and len(input_letter) == 1:
            if input_letter in user["word"]:
                for word_index in range(len(user["word"])):
                    if user["word"][word_index] == input_letter:
                        user["hidden_word"][word_index] = input_letter
            if input_letter not in user["word"]:
                user["mistakes"] += 1
                if user["mistakes"] < 10:
                    answer += f"Такой буквы нет. Попыток осталось: {10 - user['mistakes']}\n"
        else:
            answer += "Я просил всего одну букву, разве это так сложно?\n"
            await message.answer(answer)
            return
        if user["mistakes"] < 10:
            answer += "\n" + " ".join(user["hidden_word"])
            if '_' in user["hidden_word"]:
                await message.answer(answer)
                return

    if '_' in user["hidden_word"]:
        await message.answer(
            "Упс, ты програл :( \n"
            "Хочешь попробовать еще?",
            reply_markup=start_markup
        )
    else:
        await message.answer(
            "Поздравляю! Ты выиграл :) \n"
            f"Это \"{user['word']}\"\n"
            "Можешь сыграть снова",
            reply_markup=start_markup
        )
    await state.finish()


def register_handlers_game(dp: Dispatcher):
    dp.register_callback_query_handler(game_initialize, lambda c: c.data == "play", state="*")
    dp.register_message_handler(game_letter_chosen, state=GameState.in_process)
