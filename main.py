# discord bot that connects to alpaca30b via langchain and supports slash commands
import discord
from discord import app_commands
# we use json to store bot related data
import json
# we also want to get stuff from apis
import requests
# now the necessary imports for llama-cpp-python
from llama_cpp import Llama

# necessary discord stuff
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# load the model
model = "/media/anachronox/Volume/alpaca.cpp/alpaca linux/ggml-alpaca7B-q4_0.bin"
llm = Llama(model_path=model)

# now the slash command to pass the prompt to alpaca30b
@tree.command(name = "alpaca30b", description = "Get a response from alpaca30b")
async def alpaca7b(interaction, prompt: str):
    print(prompt)
    interaction.response.defer()
    # get the prompt into the right format (Q: prompt A: )
    prompt = "Q: " + prompt + " A: "
    # get the prompt from the user which is everything after the command they sent in python
    output = llm(prompt, max_tokens=32, stop=["Q:", "\n"], echo=True, top_k=200)
    # the output is in json format so we need to extract the text, which is in the text key under choices and everything after A:
    await interaction.response.send_message(output["choices"][0]["text"].split("A: ")[1])

@tree.command(name = "pyping", description = "Responds with Pong")
async def ping(interaction):
    await interaction.response.send_message("Pong! (From Perihelion)")
    
@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")
    
# we run the bot with the token from the json file
client.run(json.load(open("config.json"))["token"])