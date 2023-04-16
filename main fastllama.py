# discord bot that connects to alpaca30b via pyllamacpp and supports slash commands
import discord
from discord import app_commands
# we use json to store bot related data
import json
# we also want to get stuff from apis
import requests
# now the necessary imports for fastllama
import sys
sys.path.append("/home/anachronox/fastLLaMa/interfaces/python")
from build.fastllama import Model, ModelKind

# necessary discord stuff
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# load the model
modellocation = json.load(open("config.json"))["model"]

model = Model(
        id=ModelKind.LLAMA_7B,
        path=modellocation, #path to model
        num_threads=8, #number of threads to use
        n_ctx=512, #context size of model
        last_n_size=64, #size of last n tokens (used for repetition penalty) (Optional)
        seed=0, #seed for random number generator (Optional)
    )

# now the slash command to pass the prompt to alpaca30b
@tree.command(name = "alpaca30b", description = "Get a response from alpaca30b")
async def alpaca7b(interaction, prompt: str):
    print(prompt)
    
    prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
""" + prompt + """

### Response:
    
    """
    
    res = model.ingest(prompt, is_system_prompt=True) #ingest model with prompt
    
    
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