# discord bot that connects to alpaca30b via pyllamacpp and supports slash commands
import discord
from discord import app_commands
# we use json to store bot related data
import json
# we also want to get stuff from apis
import requests
# now the necessary imports for pyllamacpp
from pyllamacpp.model import Model

# necessary discord stuff
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# load the model
modellocation = json.load(open("config.json"))["model"]

def new_text_callback(text: str):
    print(text, end="", flush=True)

model = Model(ggml_model=modellocation, n_ctx=512)

# now the slash command to pass the prompt to alpaca30b
@tree.command(name = "alpaca30b", description = "Get a response from alpaca30b")
async def alpaca7b(interaction, prompt: str):
    print(prompt)
    
    res = model.generate(prompt, n_predict=55)
    
    # the output is in json format so we need to extract the text, which is in the text key under choices and everything after A:
    await interaction.followup.send(res)

@tree.command(name = "pyping", description = "Responds with Pong")
async def ping(interaction):
    await interaction.response.send_message("Pong! (From Perihelion)")
    
@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")
    
# we run the bot with the token from the json file
client.run(json.load(open("config.json"))["token"])