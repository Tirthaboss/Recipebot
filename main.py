import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = '7582415476:AAEiZfK7ajFzmf30VDh0UB87rbXugqeRJEo'

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome to Recipe Finder Bot! Please select an option:')
    context.bot.send_message(chat_id=update.effective_chat.id, text='/searchbyname - Search meal by name')
    context.bot.send_message(chat_id=update.effective_chat.id, text='/searchbyfirstletter - List all meals by first letter')
    context.bot.send_message(chat_id=update.effective_chat.id, text='/lookupmeal - Lookup full meal details by id')
    context.bot.send_message(chat_id=update.effective_chat.id, text='/randommeal - Lookup a single random meal')

def search_by_name(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Enter meal name:')
    name = update.message.text
    response = requests.get(f'http://www.themealdb.com/api/json/v1/1/search.php?s={name}').json()
    if response['meals']:
        meal = response['meals'][0]
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Meal name: {meal["strMeal"]}')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Meal category: {meal["strCategory"]}')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Meal area: {meal["strArea"]}')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Meal instructions: {meal["strInstructions"]}')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Meal not found')

def search_by_first_letter(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Enter first letter:')
    letter = update.message.text
    response = requests.get(f'http://www.themealdb.com/api/json/v1/1/search.php?f={letter}').json()
    if response['meals']:
        meals = response['meals']
        for meal in meals:
            context.bot.send_message(chat_id=update.effective_chat.id, text=f'Meal name: {meal["strMeal"]}')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Meals not found')

def lookup_meal(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Enter meal id:')
    meal_id = update.message.text
    response = requests.get(f'http://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}').json()
    if response['meals']:
        meal = response['meals'][0]
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Meal name: {meal["strMeal"]}')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Meal category: {meal["strCategory"]}')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Meal area: {meal["strArea"]}')
        context.bot.send_message(chat_id=update.effective_chat.id, text=f'Meal instructions: {meal["strInstructions"]}')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Meal not found')

def random_meal(update, context):
    response = requests.get('http://www.themealdb.com/api/json/v1/1/random.php').json()
    meal = response['meals'][0]
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Meal name: {meal["strMeal"]}')
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Meal category: {meal["strCategory"]}')
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Meal area: {meal["strArea"]}')
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Meal instructions: {meal["strInstructions"]}')

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('searchbyname', search_by_name))
    dp.add_handler(CommandHandler('searchbyfirstletter', search_by_first_letter))
    dp.add_handler(CommandHandler('lookupmeal', lookup_meal))
    dp.add_handler(CommandHandler('randommeal', random_meal))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
