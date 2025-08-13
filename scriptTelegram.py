import json
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import locale
import os
from dotenv import load_dotenv


# Configuración
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")  # se reemplaza en.env
JSON_FILE = "descuentos.json"
active_chats = set()

# Configurar locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

# Funciones auxiliares (igual que antes)
def cargar_descuentos():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: No se encontró {JSON_FILE}")
        return None

def filtrar_descuentos(datos, dia_actual):
    if datos is None:
        return None
    return {
        "generales": [d for d in datos.get('descuentos_generales', []) 
                     if dia_actual in d.get('dias_aplicables', [])],
        "categorias": {k: v for k, v in datos.get('descuentos_por_categoria', {}).items() 
                      if dia_actual in v.get('dias_aplicables', [])},
        "reintegros": [r for r in datos.get('reintegros', []) 
                      if dia_actual in r.get('dias_aplicables', [])]
    }

def crear_mensaje(descuentos):
    if descuentos is None:
        return "⚠️ Error al cargar descuentos"
    
    dia = datetime.now().strftime("%A").capitalize()
    mensaje = f"🛒 <b>DESCUENTOS DEL {dia}</b>\n\n"
    
    mensaje += "💳 <b>Con tarjeta:</b>\n"
    mensaje += "\n".join(f"- {d['nombre']}: {d['porcentaje']}% ({'🟢' if d.get('acumulable', False) else '🔴'})" 
                        for d in descuentos["generales"]) or "- No hay descuentos\n"
    
    mensaje += "\n\n🏷️ <b>Por categoría:</b>\n"
    mensaje += "\n".join(f"- {v['nombre']}: {v['porcentaje']}% ({'🟢' if v.get('acumulable', True) else '🔴'})" 
                        for v in descuentos["categorias"].values()) or "- No hay descuentos\n"
    
    mensaje += "\n\n🏦 <b>Reintegros:</b>\n"
    mensaje += "\n".join(f"- {r['nombre']}: {r['porcentaje']}% ✅" 
                        for r in descuentos["reintegros"]) or "- No hay reintegros\n"
    
    return f"{mensaje}\n\n⏱️ Actualizado: {datetime.now().strftime('%H:%M:%S')}"

# Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    active_chats.add(update.effective_chat.id)
    await update.message.reply_text(
        "🔔 ¡Bienvenido! Recibirás descuentos cada 30 segundos.\n"
        "Usa /stop para pausar.",
        parse_mode="HTML"
    )

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    active_chats.discard(update.effective_chat.id)
    await update.message.reply_text("🔕 Actualizaciones pausadas. Usa /start para reactivar.")

async def enviar_actualizacion(context: ContextTypes.DEFAULT_TYPE):
    dia = datetime.now().strftime("%A").capitalize()
    descuentos = filtrar_descuentos(cargar_descuentos(), dia)
    mensaje = crear_mensaje(descuentos)
    
    for chat_id in list(active_chats):
        try:
            await context.bot.send_message(chat_id, mensaje, parse_mode="HTML")
        except:
            active_chats.discard(chat_id)

# Configuración del bot
async def post_init(application: Application):
    await application.bot.set_my_commands([
        ("start", "Inicia las actualizaciones"),
        ("stop", "Detiene las actualizaciones")
    ])
    application.job_queue.run_repeating(enviar_actualizacion, interval=30.0, first=5)

def main():
    app = Application.builder().token(TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    
    print("🤖 Bot iniciado. Usa /start en Telegram...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
