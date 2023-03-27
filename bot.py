import discord
import handle_responses
from discord.utils import find
from datetime import datetime
import os
from dotenv import find_dotenv, load_dotenv

async def send_message_to_channel(user_id, channel, response):
    try:
        if user_id != "":
            await channel.send(f"<@{user_id}>")
        if response != "_":
            await channel.send(response)
    except Exception as e:
        await channel.send("Errrrrrrror! Why can't I send anything useful?")
        print(e)


async def process_message(user, channel, user_message, client):
    try:
        response, contains_media, filename = await handle_responses.process(user_message, client)
        await send_message_to_channel(user.id, channel, response)
        if filename[-4:] not in [".png", ".mp4"] and filename != "":
            await send_message_to_channel("", channel, filename)
        if contains_media:
            await channel.send("Uploading...")
            await channel.send(f"Requested by **{str(user)}**", file=discord.File(filename))
    except Exception as e:
        await send_message_to_channel(user.id, channel, e)


def run_discord_bot():
    env_file = find_dotenv()
    load_dotenv(env_file)
    TOKEN = os.environ["TOKEN"]
    intents = discord.Intents.all()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        await client.change_presence(status=discord.Status.online, activity=discord. Activity(type=discord.ActivityType.listening, name='Commands'))
        print(f"{client.user} is saying Hi!")

    @client.event
    async def on_guild_join(guild):
        bot_help = find(lambda x: x.name == 'bot-help',  guild.text_channels)
        if bot_help and bot_help.permissions_for(guild.me).send_messages:
            await bot_help.send("@everyone")
            r1, _, r2 = await handle_responses.process("help")
            await bot_help.send(r1)
            await bot_help.send(r2)

    @client.event
    async def on_message(message):
        user = message.author
        user_message = str(message.content)
        channel = message.channel

        if message.author.bot:
            return
        else:
            print(f"{client.user} is seeing {str(message.author)} saying sth!")

        if (user_message[0:3] == 'f::'):
            await client.change_presence(status=discord.Status.do_not_disturb, activity=discord. Activity(type=discord.ActivityType.watching, name='Magic happens'))
            with open("logger.txt", "a") as logger:
                ctime = datetime.now()
                str_ctime = ctime.strftime("%Y-%m-%d %H:%M:%S")
                log = f"{str_ctime} -> {str(message.author)}: {user_message}"
                logger.write(log + "\n")

            user_message = user_message[3:].strip()
            await process_message(user, channel, user_message, client)
            await client.change_presence(status=discord.Status.online, activity=discord. Activity(type=discord.ActivityType.listening, name='Commands'))

    client.run(TOKEN)
