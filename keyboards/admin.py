"""Клавиатуры для Администратора"""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models import User 
from typing import List, Tuple

KB = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить инспектора"),
            KeyboardButton(text="Показать инспекторов"),
        ],
        [
            KeyboardButton(text="Добавить администратора"),
            KeyboardButton(text="Показать администраторов"),
        ],
    ],
    resize_keyboard=True,
)

def get_inspectors_buttons_keyboard(
    inspectors: List[User], 
    page: int = 0, 
    page_size: int = 10
) -> Tuple[str, InlineKeyboardBuilder]:
    total_pages = (len(inspectors) + page_size - 1) // page_size
    start_idx = page * page_size
    end_idx = start_idx + page_size
    page_inspectors = inspectors[start_idx:end_idx]
    
    # Формируем текст сообщения
    text = f"<b>Список инспекторов (страница {page + 1} из {total_pages}):</b>"
    
    # Создаем клавиатуру
    builder = InlineKeyboardBuilder()
    
    # Добавляем кнопки с инспекторами
    for inspector in page_inspectors:
        full_name = f"{inspector.first_name or ''} {inspector.last_name or ''}".strip()
        if not full_name:
            full_name = inspector.username or "Без имени"
        builder.button(
            text=full_name,
            url=f"https://t.me/{inspector.username}" if inspector.username else None,
            callback_data=f"inspector_{inspector.id}" if not inspector.username else None
        )
    
    # Делаем кнопки в 1 колонку
    builder.adjust(1)
    
    # Кнопки пагинации
    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(InlineKeyboardButton(text="Назад", callback_data=f"insp_page_{page - 1}"))
    if page < total_pages - 1:
        pagination_buttons.append(InlineKeyboardButton(text="Вперед ", callback_data=f"insp_page_{page + 1}"))
    
    if pagination_buttons:
        builder.row(*pagination_buttons)
    
    
    return text, builder