import discord
from discord import app_commands
import requests

# === НАСТРОЙКИ ===
DISCORD_TOKEN = "MTQzNzQxODg5NzU4MTAxOTI5Ng.G3_U0B.DzD0pkxzT2jCIzH5p9vqNIrO0EjSYcnq_AWuqw"
LUARMOR_API_KEY = "d0b09e8811b852c671c2ee5b796ab3f5eb429147dc056163e25e"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    print(f"✅ Бот запущен как {client.user}")
    try:
        synced = await tree.sync()
        print(f"🔧 Синхронизированы команды: {len(synced)}")
    except Exception as e:
        print(e)


@tree.command(name="hwid", description="Сбросить HWID по ключу Luarmor")
async def hwid_reset(interaction: discord.Interaction, key: str):
    await interaction.response.defer()
    await interaction.followup.send("🔄 Отправляю запрос на сброс HWID...")

    url = "https://api.luarmor.net/v3/hwid/reset"
    headers = {"Authorization": f"Bearer {LUARMOR_API_KEY}"}
    payload = {"license_key": key}

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        if response.status_code == 200 and data.get("success"):
            await interaction.followup.send("✅ HWID успешно сброшен!")
        else:
            msg = data.get("message", "Не удалось сбросить HWID.")
            await interaction.followup.send(f"⚠️ Ошибка: {msg}")

    except Exception as e:
        await interaction.followup.send(f"❌ Ошибка при обращении к API: {e}")


client.run(DISCORD_TOKEN)
