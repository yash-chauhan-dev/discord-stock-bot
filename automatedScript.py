from discord.ext import commands
from discord import Intents
from dotenv import load_dotenv
from channelConst import CHANNEL_ID
from datetime import datetime, timedelta, time
import asyncio
import os
from botFunctions import graph, get_eod_data, last_hour, compare


class DailyUpdates():
    def __init__(self, company_code, channel):
        self.company_code = company_code
        self.channel = channel

    async def eod_data_update(self):
        await graph(ctx = self.channel, company_name = self.company_code)
        await last_hour(ctx = self.channel, company_name = self.company_code)
        await get_eod_data(ctx = self.channel, company_name = self.company_code)

class Bot():
    def __init__(self):
        load_dotenv()
        self.TOKEN = os.getenv("DISCORD_TOKEN")
        self.GUILD = os.getenv("DISCORD_GUILD")
        intents = Intents().default()
        intents.members = True
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='!', intents=intents)

    def get_channel(self, id):
        return self.bot.get_channel(id)

async def called_once_a_day(obj):  # Fired every day
        for id in CHANNEL_ID:
            channel = obj.get_channel(CHANNEL_ID[id])
            daily_updates = DailyUpdates(channel = channel, company_code = id)
            await daily_updates.eod_data_update()

async def background_task(obj):
    WHEN = time(22,30,0) # 4:00 PM IST (10:30 PM UTC)
    now = datetime.utcnow()
    if now.time() > WHEN:  # Make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start 
    while True:
        now = datetime.utcnow() # You can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        target_time = datetime.combine(now.date(), WHEN)  # 10:30 PM today (In UTC)
        seconds_until_target = (target_time - now).total_seconds()
        await asyncio.sleep(seconds_until_target)  # Sleep until we hit the target time
        await called_once_a_day(obj)  # Call the helper function that sends the message
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        seconds = (tomorrow - now).total_seconds()  # Seconds until tomorrow (midnight)
        await asyncio.sleep(seconds)   # Sleep until tomorrow and then the loop will start a new iteration

async def main():
    bot_obj = Bot()
    bot = bot_obj.bot

    async with bot:
        bot.loop.create_task(background_task(bot_obj))

        @bot_obj.bot.event
        async def on_ready():
            print("--BOT RUNNING--")

        @bot_obj.bot.command(name="CH")
        async def compare_history(ctx, company):
            if ctx.channel.name == "compare-stocks-history":
                company_list = [x.strip() for x in company.split(",")]
                company_list = list(filter(None, company_list))

                await compare(ctx, company_list)

        @bot_obj.bot.command(name="G")
        async def stock_graph(ctx, company):
            if ctx.channel.name == "compare-stocks-history":

                await graph(ctx, company)

        @bot_obj.bot.command(name="clx")
        async def clear(ctx):
            if ctx.message.author == ctx.guild.owner:
                await ctx.channel.purge()

        await bot.start(bot_obj.TOKEN)


if __name__ == "__main__":

    asyncio.run(main())
