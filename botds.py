import os
import requests
import discord
from discord import app_commands

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
LUARMOR_API_KEY = os.getenv("LUARMOR_API_KEY")
PROJECT_ID = "79bf4877bc7902f5807fcd4dcb2d8881"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f"✅ Бот запущен как {client.user}")
    await tree.sync()
    print("🔧 Команды синхронизированы")

@tree.command(name="hwid", description="Сбросить HWID по ключу Luarmor")
async def hwid_reset(interaction: discord.Interaction, key: str):
    await interaction.response.defer()
    await interaction.followup.send("🔄 Отправляю запрос на сброс HWID...")

    url = f"https://api.luarmor.net/v3/projects/{PROJECT_ID}/users/resethwid"
    headers = {
        "Authorization": f"Bearer {LUARMOR_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "user_key": key
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        data = response.json()

        if response.status_code == 200 and data.get("success"):
            await interaction.followup.send("✅ HWID успешно сброшен!")
        else:
            msg = data.get("message", "Не удалось сбросить HWID.")
            await interaction.followup.send(f"⚠️ Ошибка: {msg}")
    except Exception as e:
        await interaction.followup.send(f"❌ Ошибка при обращении к API: {e}")

client.run(DISCORD_TOKEN)
