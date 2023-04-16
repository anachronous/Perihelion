# discord bot that connects to alpaca30b via langchain and supports slash commands
import discord
from discord import app_commands
# we use json to store bot related data
import json
# we also want to get stuff from apis
import requests
# now the necessary imports for langchain
from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig, pipeline
from langchain.llms import HuggingFacePipeline
from langchain import PromptTemplate, LLMChain
import torch

# necessary discord stuff
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# load the model
model = "/media/anachronox/Volume/alpaca.cpp/alpaca linux/ggml-alpaca7B-q4_0.bin"
tokenizer = LlamaTokenizer.from_pretrained(model)

base_model = LlamaForCausalLM.from_pretrained(
                model,
                load_in_8bit=True,
                device_map="auto" 
                                    )

# create the pipeline
pipe = pipeline(
    "text-generation",
    model=base_model, 
    tokenizer=tokenizer, 
    max_length=512,
    temperature=0.6,
    top_p=0.95,
    repetition_penalty=1.2
)

local_llm = HuggingFacePipeline(pipeline=pipe)

# create prompt template
template = """Below is an instruction that describes a task. Write a response that appropriately completes the request.

### Instruction: 
{instruction}

Answer:"""

prompt = PromptTemplate(template=template, input_variables=["instruction"])

# create the chain
llm_chain = LLMChain(prompt=prompt, 
                     llm=local_llm
                     )

# now the slash command to pass the prompt to alpaca30b
@tree.command(name = "alpaca30b", description = "Get a response from alpaca30b")
async def alpaca30b(interaction):
    # get the prompt from the user which is everything after the command
    prompt = interaction.data["options"][0]["value"]
    # pass it to alpaca30b
    response = llm_chain(prompt)
    # send the response back to the user
    await interaction.response.send_message(response)

@tree.command(name = "pyping", description = "Responds with Pong")
async def ping(interaction):
    await interaction.response.send_message("Pong! (From Perihelion)")
    
@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")
    
# we run the bot with the token from the json file
client.run(json.load(open("config.json"))["token"])