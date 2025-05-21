"""Список инспекторов"""

from aiogram import Router, F
from aiogram.types import Message
from database.models import User, UserRole
from filters.admin import IsAdmin
from filters.inspector import IsInspector
from aiogram.types import CallbackQuery
from keyboards.admin import get_inspectors_buttons_keyboard


router = Router()


@router.message(F.text == "Показать инспекторов", IsAdmin())
async def show_inspectors(message: Message):
    """Отображает список инспекторов с пагинацией в виде кнопок"""
    inspectors = list(User.select().join(UserRole).where(UserRole.role == IsInspector.role))
    
    if not inspectors:
        await message.answer("Список инспекторов пуст.")
        return
    
    text, keyboard = get_inspectors_buttons_keyboard(inspectors)
    await message.answer(
        text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("insp_page_"))
async def handle_inspectors_page(callback: CallbackQuery):
    page = int(callback.data.split("_")[2])
    inspectors = list(User.select().join(UserRole).where(UserRole.role == IsInspector.role))
    
    text, keyboard = get_inspectors_buttons_keyboard(inspectors, page)
    await callback.message.edit_text(
        text,
        reply_markup=keyboard.as_markup(),
        parse_mode="HTML"
    )
    await callback.answer()
    