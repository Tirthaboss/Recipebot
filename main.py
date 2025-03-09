"""import requests
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
"""
import streamlit as st
import pandas as pd

# Sample recipe database
recipes = [
    {
        "name": "Vegetable Stir Fry",
        "ingredients": ["broccoli", "carrot", "bell pepper", "soy sauce"],
        "dietary_restrictions": ["vegan", "gluten-free"],
        "cuisine": "Asian"
    },
    {
        "name": "Chicken Salad",
        "ingredients": ["chicken", "lettuce", "tomato", "olive oil"],
        "dietary_restrictions": ["gluten-free"],
        "cuisine": "Mediterranean"
    },
    {
        "name": "Pasta Primavera",
        "ingredients": ["pasta", "zucchini", "bell pepper", "olive oil"],
        "dietary_restrictions": ["vegetarian"],
        "cuisine": "Italian"
    },
    {
        "name": "Quinoa Bowl",
        "ingredients": ["quinoa", "black beans", "corn", "avocado"],
        "dietary_restrictions": ["vegan", "gluten-free"],
        "cuisine": "Mexican"
    },
    {
        "name": "Beef Tacos",
        "ingredients": ["beef", "taco shells", "lettuce", "cheese"],
        "dietary_restrictions": [],
        "cuisine": "Mexican"
    }
]

# Convert to DataFrame for easier manipulation
recipes_df = pd.DataFrame(recipes)

# Streamlit app
st.title("Recipe Suggestion System")

# User inputs
available_ingredients = st.text_input("Enter available ingredients (comma-separated):")
dietary_restrictions = st.multiselect("Select dietary restrictions:", ["vegan", "vegetarian", "gluten-free", "dairy-free", "nut-free"])

if st.button("Suggest Recipes"):
    if available_ingredients:
        available_ingredients_list = [ingredient.strip().lower() for ingredient in available_ingredients.split(",")]
        
        # Filter recipes based on available ingredients and dietary restrictions
        suggested_recipes = []
        
        for index, row in recipes_df.iterrows():
            ingredients = row['ingredients']
            restrictions = row['dietary_restrictions']
            
            # Check if all ingredients are available
            if all(item in available_ingredients_list for item in ingredients):
                # Check if dietary restrictions are satisfied
                if all(restriction in restrictions for restriction in dietary_restrictions):
                    suggested_recipes.append(row['name'])
        
        if suggested_recipes:
            st.success("Suggested Recipes:")
            for recipe in suggested_recipes:
                st.write(f"- {recipe}")
        else:
            st.warning("No recipes found based on your criteria.")
    else:
        st.warning("Please enter at least one ingredient.")
