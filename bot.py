import re
import discord
import asyncio
import sys
import os
import logging
import colorama
from colorama import Fore
import ctypes
import random
import os

logging.basicConfig(level=logging.WARNING)
logging.getLogger('discord').setLevel(logging.WARNING)
logging.getLogger('discord.gateway').setLevel(logging.WARNING)
logging.getLogger('discord.client').setLevel(logging.WARNING)
logging.getLogger('discord.http').setLevel(logging.WARNING)



# defining the colors
r = Fore.LIGHTRED_EX
y = Fore.LIGHTYELLOW_EX
g = Fore.LIGHTGREEN_EX
res = Fore.RESET

BOT_UID = 1303161693043560458
DIVISOR = 99
TIME = 4
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print(f"Error checking admin status: {e}")
        return False

def elevate_privileges():
    if not is_admin():
        try:
            script = os.path.abspath(sys.argv[0])
            params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script}" {params}', None, 1
            )
            sys.exit(0)
        except Exception as e:
            print(f"Failed to elevate privileges: {e}")
            sys.exit(1)

if __name__ == "__main__":
    elevate_privileges()
    print("Running with admin privileges!")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("discord")

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

client = discord.Client()

with open("tokens.txt", "r") as file:
    TOKEN = file.read().strip()

    print(f"[{y}!{res}] Checking tokens in 'tokens.txt'...")

WHITELISTED_CHANNELS = [1331273098552545310]

EMOJI_TO_WORD = {
    "2052whiteleft": "left",
    "7373whitedown": "down",
    "9847whiteright": "right",
    "4695whiteup": "up",
}

COMMANDS = [
    ",cf {amount} heads",
    ",gamble {amount}",
    ",roll {amount}",
    ",supergamble {amount}",
    ",work",
    ",crime",
    ",cf {amount} tails",
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

clear_screen()

banner = """
                 ▄████  ██▀███  ▓█████ ▓█████ ▓█████▄        █████▒▄▄▄       ██▀███   ███▄ ▄███▓
                ██▒ ▀█▒▓██ ▒ ██▒▓█   ▀ ▓█   ▀ ▒██▀ ██▌     ▓██   ▒▒████▄    ▓██ ▒ ██▒▓██▒▀█▀ ██▒
               ▒██░▄▄▄░▓██ ░▄█ ▒▒███   ▒███   ░██   █▌     ▒████ ░▒██  ▀█▄  ▓██ ░▄█ ▒▓██    ▓██░
               ░▓█  ██▓▒██▀▀█▄  ▒▓█  ▄ ▒▓█  ▄ ░▓█▄   ▌     ░▓█▒  ░░██▄▄▄▄██ ▒██▀▀█▄  ▒██    ▒██ 
               ░▒▓███▀▒░██▓ ▒██▒░▒████▒░▒████▒░▒████▓  ██▓ ░▒█░    ▓█   ▓██▒░██▓ ▒██▒▒██▒   ░██▒
                ░▒   ▒ ░ ▒▓ ░▒▓░░░ ▒░ ░░░ ▒░ ░ ▒▒▓  ▒  ▒▓▒  ▒ ░    ▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ▒░   ░  ░
                 ░   ░   ░▒ ░ ▒░ ░ ░  ░ ░ ░  ░ ░ ▒  ▒  ░▒   ░       ▒   ▒▒ ░  ░▒ ░ ▒░░  ░      ░
               ░ ░   ░   ░░   ░    ░      ░    ░ ░  ░  ░    ░ ░     ░   ▒     ░░   ░ ░      ░   
                     ░    ░        ░  ░   ░  ░   ░      ░               ░  ░   ░            ░   
                                               ░        ░                                       
"""
print(f"{Fore.CYAN}{banner}{Fore.RESET}")

def parse_cooldown(embed):
    if "cooldown" in embed.description:
        match = re.search(r"``([\d.]+)s``", embed.description)
        if match:
            return float(match.group(1))
    return None

def extract_emoji_id(emoji: str) -> str:
    match = re.search(r"<:(\d+)>", emoji)
    return match.group(1) if match else None

def parse_embed(embed):
    if embed.title == "Dance Mode!" and "**Combo:**" in embed.description:
        combo_line = embed.description.split("**Combo:**")[-1].strip()
        emojis = re.findall(r"<:(\d+\w+):\d+>", combo_line)
        directions = [EMOJI_TO_WORD.get(emoji, "") for emoji in emojis]
        return " ".join(filter(None, directions))
    return None

def parse_money_embed(description):
    match = re.search(r'`(\d+)`', description)
    if match:
        return int(match.group(1))
    return None


import re

def parse_work_message(description):
    
    match = re.search(r"you worked as.*?and earned \*\*[\$]([0-9,]+)\*\*", description)
    if match:
        earnings = match.group(1)  
        return earnings
    return None

async def handle_work_command(embed):
    if "you worked as a" in embed.description:
        match = re.search(r"you worked as a (.*?) and earned \*\*[\$]([0-9,]+)\*\*", embed.description)
        if match:
            job = match.group(1)
            earnings = match.group(2)
            print(f"Worked as a {job}, earned {earnings}")
            next_command = ",gamble 100"
            return next_command
    return None

@client.event
async def on_ready():
    if WHITELISTED_CHANNELS:
        channel = client.get_channel(WHITELISTED_CHANNELS[0])
        if channel:
            print(f"[{g}+{res}] Logged in with Token {TOKEN}.\n[{g}+{res}] Starting Autofarm in channel ID: {channel.id}")
            await channel.send(",dance")
        else:
            print(f"[{r}!{res}] Failed to find channel with ID: {WHITELISTED_CHANNELS[0]}")

@client.event
async def on_message(message):
    try:
        for embed in message.embeds:
            dance_response = parse_embed(embed)
            if dance_response:
                print(f"[{y}!{res}] Sending dance response: {dance_response}")
                await message.channel.send(dance_response)

            money_response = parse_money_embed(embed.description)
            if money_response:
                print(f"[{g}+{res}] Extracted money value: {money_response}")
                random_command = random.choice(COMMANDS)
                response_command = random_command.replace("{amount}", str(money_response))
                print(f"[{g}+{res}] Sending command: {response_command}")
                await message.channel.send(response_command)

                            
            earnings = parse_work_message(embed.description)
            if earnings:
                print(f"[{g}+{res}] Extracted earnings: ${earnings}")
                random_command = random.choice(COMMANDS)
                response_command = random_command.replace("{amount}", earnings)
                print(f"[{g}+{res}] Sending command: {response_command}")
                await message.channel.send(response_command)

                
                follow_up_command = random.choice(COMMANDS)
                print(f"[{g}+{res}] Sending follow-up command: {follow_up_command}")
                await message.channel.send(follow_up_command)
                    
        
                
                follow_up_command = random.choice(COMMANDS)
                print(f"[{g}+{res}] Sending follow-up command: {follow_up_command}")
                await message.channel.send(follow_up_command)

    except Exception as e:
        print(f"[{r}-{res}]Error processing message: {e}")


async def repeat_actions():
    while True:
        await asyncio.sleep(TIME)  
        print(f"[{y}!{res}] Repeating actions...")
        
        
        random_command = random.choice(COMMANDS)
        
     
        if "{amount}" in random_command:
            amount = random.randint(100, 1000) 
            random_command = random_command.replace("{amount}", str(amount))
        
        print(f"[{g}+{res}] Sending random command: {random_command}")
        

        channel = client.get_channel(WHITELISTED_CHANNELS[0])
        if channel:
            await channel.send(random_command)



async def start_bot():
    await asyncio.gather(client.start(TOKEN), repeat_actions())

asyncio.run(start_bot())
