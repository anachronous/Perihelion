# discord bot that connects to alpaca30b via langchain and supports slash commands
import discord
from discord import app_commands
import math
import string
import embeds
import zimath as zim
import zidice as zid
import random
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
model = json.load(open("config.json"))["model"]
llm = Llama(model_path=model)

# now the slash command to pass the prompt to alpaca7b
@tree.command(name = "alpaca13b", description = "Get a response from alpaca13b")
async def alpaca13b(interaction, prompt: str):
    print(prompt)
    ogprompt = prompt
    
    # check if the channel id is 768600365602963496
    if interaction.channel_id == 768600365602963496:
        # if it is send an ephemeral message to the user, saying that they can't use this command in this channel and return
        await interaction.response.send_message("You can't use this command in this channel! Move to #bot-fun instead.", ephemeral=True)
        return
    
    # get the prompt into the right format (Q: prompt A: )
    prompt = "Q: " + prompt + " A: "
    await interaction.response.send_message("Your prompt: " + ogprompt)
    # get the prompt from the user which is everything after the command they sent in python
    output = llm(prompt, max_tokens=450, stop=["Q: ", "\n"], echo=True)
    # the output is in json format so we need to extract the text, which is in the text key under choices and everything after A:
    await interaction.followup.send(output["choices"][0]["text"].split("A: ")[1])

@tree.command(name = "pyping", description = "Responds with Pong")
async def ping(interaction):
    await interaction.response.send_message("Pong! (From Perihelion)")
    
#########################################
### Dice commands with slash commands ###
#########################################

# help command for the dice commands, that explains the notation
# we do this with an embed
@tree.command(name = "dicehelp", description = "Arguments for the dice commands")
async def dicehelp(interaction):
    await interaction.response.send_message(embed=embeds.dice_help(), ephemeral=True)

@tree.command(name = "probroll", description = "Calculates the probability of rolling the given number for the given dice roll.")
async def probroll(interaction, roll: str, result: int):
    print(roll)
    
    # split the dice notation into a list split at the d
    dice_notation_list = roll.split('d')
    # get the number of dice and convert it to an integer
    number_of_dice = int(dice_notation_list[0])
    # get the number of sides and convert it to an integer
    number_of_sides = int(dice_notation_list[1])
    # calculate the probability of rolling the roll
    # we use uspensky's formula (https://www.gigacalculator.com/calculators/dice-probability-calculator.php)
    probability = zim.uspensky_formula(result, number_of_dice, number_of_sides)
    # send the probability to the user as an ephemeral message
    await interaction.response.send_message(roll + ": " + f'{probability * 100:.2f}%', ephemeral=True)

@tree.command(name = "roll", description = "Rolls the given dice notation.")
async def roll(interaction, roll: str):
    total = zid.roll(roll)
            
    # we now send the total
    await interaction.response.send_message(roll + ": " + total)
    
# rolls diceset
@tree.command(name = "diceset", description = "Rolls the given dice set.")
async def diceset(interaction, diceset: str):
    # for example: !diceset 1d20 + 1d4 + 1d6
    # would produce a message like this:
    # 1d20: 10
    # 1d4: 3
    # 1d6: 5
    # the total is 18
    rolls = zid.rollset(diceset)
    # we go through each dice type in the dictionary
    message_string = ""
    for dice_type in rolls:
        # we add the dice type to the string
        message_string += 'd' + str(dice_type) + ': '
        # we go through each roll in the list and add it to the string
        for roll in rolls[dice_type]:
            message_string += str(roll) + ', '
        # we remove the last comma and space
        message_string = message_string[:-2]
        # we add a new line
        message_string += '\n'
    # we remove the last new line
    message_string = message_string[:-1]
    # we send the message
    await interaction.response.send_message("Input: " + diceset + "\n" + message_string)
    
# gets the average of a dice roll by simulating it a lot of times
@tree.command(name = "averageslow", description = "Gets the average of a dice roll by simulating it a lot of times.")
async def averageslow(interaction, dice_notation: str, times: int):
    # send an ephemeral thinking message because this can take a while
    await interaction.response.send_message("Thinking...", ephemeral=True)

    # we use the average_roll_simulator function from zidice.py to get the average rounded to 3 decimal places
    average = round(zid.average_roll_simulator(dice_notation, times), 3)

    # we now send the average as a message
    await interaction.followup.send('The average is ' + str(average) + ' for ' + str(times) + ' rolls of (' + dice_notation + ')')
    
# probroll but with simulation
@tree.command(name = "probrollslow", description = "Calculates the probability by simulating it a lot of times.")
async def probrollslow(interaction, flag: str, dice_notation: str, target: int, times: int):
    # send an ephemeral thinking message because this can take a while
    await interaction.response.send_message("Thinking...", ephemeral=True)
    
    # we now use the roll_simulator function from zidice.py to get a dictionary of the results
    roll_dict = zid.roll_simulator(dice_notation, times)
    
    # we now iterate through the dictionary and count how many results are what we want
    # we use the argument to determine if we want to get the results that are equal, higher or lower than the target
    # at the same time we also count the total amount of rolls, so we can divide the amount of results we want by the total amount of rolls to get the probability
    amount = 0
    total = 0
    for (key, value) in roll_dict.items():
        if (flag == 'h' and key > target) or (flag == 'l' and key < target) or ((flag != 'h' or flag != "l") and key == target):
            amount += value
        total += value
        
    # we now calculate the probability
    probability = amount / total
    # we now send the probability as a message in percent rounded to 3 decimal places
    await interaction.followup.send('The probability is ' + str(round(probability * 100, 3)) + '%' + ' for ' + str(times) + ' rolls of (' + dice_notation + ')' + ' with a target of ' + str(target) + ' and a flag of ' + flag + ".")
    
# dpr calculation using simulation
# takes a list of dice notations, a to hit value, an ac value, a crit range and a number of simulations and returns the dpr
# @tree.command(name = "dprslow", description = "Calculates the dpr by simulating it a lot of times.")
# async def dprslow(interaction, damage: str, to_hit: int, ac: int, crit_range: str, meaningful_crits: bool, times: int):
    

    
@client.event
async def on_ready():
    await tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Perihelion"))
    print("Ready!")
    
# we run the bot with the token from the json file
client.run(json.load(open("config.json"))["token"])