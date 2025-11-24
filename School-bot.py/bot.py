from json import JSONDecodeError

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_TOKEN ,ADMINS, COMPLAINTS_FILE
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import datetime
import json

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

class ComplaintForm(StatesGroup):
    waiting_for_text = State()

#MAIN MENU
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="🏫 Мектеп туралы")
    kb.button(text="📑 Сабақ кестесі")
    kb.button(text="❓ Жиі қойылатын сұрақтар")
    kb.button(text="🔐 Анонимді хабар жіберу")
    kb.button(text="📞 Кері байланыс контактілері")
    kb.adjust(2, 1, 1, 1)

    await message.answer(
        "Сәлем, бұл №219 ЖББ мектептің телеграм боты. Келесі батырмалардың бірін таңда: ",
        reply_markup=kb.as_markup(resize_keyboard=True)
    )

@dp.message(lambda msg: msg.text == "🏫 Мектеп туралы")
async def about_school(message: types.Message):
    await message.answer("text about school")

#LESSONS
@dp.message(lambda msg: msg.text == "📑 Сабақ кестесі")
async def lessons(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="10 A", callback_data="les_ona"),
            InlineKeyboardButton(text="10 Ә", callback_data="les_onae")
        ],
        [
            InlineKeyboardButton(text="9 A", callback_data="les_togyza"),
            InlineKeyboardButton(text="9 Ә", callback_data="les_togyzae")
        ],
        [InlineKeyboardButton(text="🔙 Артқа", callback_data="back_main")]
    ])

    await message.answer("Керек сыныпты таңда:", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("les_"))
async def subjects(callback: types.CallbackQuery):
    if callback.data == "les_ona":
        await callback.message.answer("Сабақ кестесі #1")
    if callback.data == "les_onae":
        await callback.message.answer("Сабақ кестесі #2")
    if callback.data == "les_togyza":
        await callback.message.answer("Сабақ кестесі #3")
    if callback.data == "les_togyzae":
        await callback.message.answer("Сабақ кестесі #4")

    await callback.answer()

#FAQ
@dp.message(lambda msg: msg.text == "❓ Жиі қойылатын сұрақтар")
async def faq_menu(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❓ question1", callback_data="faq_q1")
        ],
        [
            InlineKeyboardButton(text="❓ question2", callback_data="faq_q2")
        ],
        [
            InlineKeyboardButton(text="❓ question3", callback_data="faq_q3")
        ],
        [
            InlineKeyboardButton(text="❓ question4", callback_data="faq_q4")
        ],
        [InlineKeyboardButton(text="🔙 Артқа", callback_data="back_main")]

    ])

    await message.answer("Керек сұрақты таңданыз: ", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("faq_"))
async def answers(callback: types.CallbackQuery):
    if callback.data == "faq_q1":
        await callback.message.answer("Сабақ кестесі #1")
    if callback.data == "faq_q2":
        await callback.message.answer("Сабақ кестесі #2")
    if callback.data == "faq_q3":
        await callback.message.answer("Сабақ кестесі #3")
    if callback.data == "faq_q4":
        await callback.message.answer("Сабақ кестесі #4")

    await callback.answer()


@dp.message(lambda msg: msg.text =="📞 Кері байланыс контактілері")
async def contacts(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Мектеп директоры", callback_data="con_n1")
        ],
        [
            InlineKeyboardButton(text="Мектеп завучі", callback_data="con_n2")
        ],
        [
            InlineKeyboardButton(text="Мектеп психологы", callback_data="con_n3")
        ],
        [
            InlineKeyboardButton(text="Бот туралы көмек ", callback_data="con_n4")
        ],
        [InlineKeyboardButton(text="🔙 Артқа", callback_data="back_main")]
    ])
    await message.answer("Керек контактты таңда: ", reply_markup=kb)


@dp.callback_query(lambda c: c.data.startswith("con_"))
async def contact(callback: types.CallbackQuery):
    if callback.data == "con_n1":
        await callback.message.answer("director info")
    if callback.data == "con_n2":
        await callback.message.answer("zavuch info")
    if callback.data == "con_n3":
        await callback.message.answer("psychologist info")
    if callback.data == "con_n4":
        await callback.message.answer("help with bot")

    await callback.answer()

@dp.callback_query(lambda c: c.data == "back_main")
async def back_to_main(callback: types.CallbackQuery):
    await start_cmd(callback.message)
    await callback.answer()

@dp.message(lambda msg: msg.text == "🔐 Анонимді хабар жіберу")
async def anonym(message: types.Message, state: FSMContext):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Артқа", callback_data="back_main")]
    ])
    await message.answer("Келесі хабарламада сізді мазалаған жағдайды қарапайым тілмен жазып жіберіңіз. Не болғанын, кіммен болғанын және қашан болғанын айтсаңыз, біз жағдайды тезірек түсіне аламыз. Шағымыңыз толықтай құпия сақталады 🔐", reply_markup=kb)
    await state.set_state(ComplaintForm.waiting_for_text)

@dp.message(ComplaintForm.waiting_for_text)
async def recieve_complaint(message: types.Message, state: FSMContext):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Бастапқы менюға қайту", callback_data="back_main")]
    ])
    complaint_text = message.text
    user_id = message.from_user.id
    curenttime = datetime.datetime.now().strftime("%H:%M:%S")
    new_data = {
        "user_id": user_id,
        "complaint": complaint_text,
        "time": curenttime
    }

    try:
       with open(COMPLAINTS_FILE, "r", encoding='utf-8') as f:
           complaints = json.load(f)
    except (JSONDecodeError, FileNotFoundError):
        complaints = []

    complaints.append(new_data)

    with open(COMPLAINTS_FILE, "w", encoding='utf-8') as f:
        json.dump(complaints, f, indent=2, ensure_ascii=False)

    await message.answer("Шағым қабылданды! Мәселені шешуге көмектесеміз!", reply_markup=kb)
    await state.clear()

@dp.message(Command("admin"))
async def admin_cmd(message: types.Message):
    user_id = message.from_user.id

    if user_id in ADMINS:
        try:
            with open(COMPLAINTS_FILE, "r", encoding='utf-8') as f:
                complaints = json.load(f)
        except (FileNotFoundError, JSONDecodeError):
            await message.answer("No complains")
            return

        text = "\n".join(f"{c}" for c in complaints)
        await message.answer(text)
    else:
        await message.answer("Кіруге рұқсат жоқ!")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())