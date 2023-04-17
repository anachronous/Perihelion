import discord

# help command for dice commands, is imported in main_llama-cpp-py.py
def dice_help():
    embed=discord.Embed()
    embed.add_field(name=".droplowest(x)", value="drops the lowest x rolls", inline=True)
    embed.add_field(name=".drophighest(x)", value="drops the highest x rolls", inline=True)
    embed.add_field(name=".reroll(x)", value="rerolls any rolls that are x until they're different", inline=True)
    embed.add_field(name=".rerollonce(x)", value="rerolls any rolls that are x once", inline=True)
    embed.add_field(name=".keeplowest(x)", value="keeps the lowest x rolls", inline=True)
    embed.add_field(name=".keephighest(x)", value="keeps the highest x rolls", inline=True)
    embed.add_field(name="Flag h", value="higher than the target", inline=True)
    embed.add_field(name="Flag l", value="lower than the target", inline=True)
    embed.set_footer(text="Dice Command Arguments")
    return embed