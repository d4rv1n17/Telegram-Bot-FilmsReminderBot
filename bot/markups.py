from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btnMAIN = KeyboardButton("⬅️Main menu")


# --- Main Menu --- #
btnFavorites = KeyboardButton("/Favorites📁")
btnOther = KeyboardButton("➡️Other")
btnTop_Films = KeyboardButton("/Top25📊")
main_menu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnFavorites, btnTop_Films, btnOther)


# --- Other Menu --- #
btnSubscribe = KeyboardButton("/Subscribe✅")
btnUnsubscribe = KeyboardButton("/Unsubscribe❌")
btnCommands = KeyboardButton("Commands📜")
btnHelp = KeyboardButton("🆘Help")
other_menu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnMAIN, btnSubscribe, btnUnsubscribe, btnCommands, btnHelp)


# --- Subscribe Menu --- #
subscribe_menu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnSubscribe, btnUnsubscribe)