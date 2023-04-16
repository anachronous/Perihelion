import random
import zimath as zim

def rollset(dice_notation):
    # this command rolls the specified dice similarly to roll but returns the rolls instead of the sum
    # the modifiers are:
    # .droplowest(x) - drops the lowest x rolls
    # .drophighest(x) - drops the highest x rolls
    # .reroll(x) - rerolls any rolls that are x until they're different
    # .rerollonce(x) - rerolls any rolls that are x once
    # .keeplowest(x) - keeps the lowest x rolls
    # .keephighest(x) - keeps the highest x rolls
    # we first split the dice_notation into a list

    message_parts = dice_notation.split(" ")
    # we create a dictionary to store the rolls
    # the key is the dice type (eg d8) and the value is a list of the rolls of that type (eg [1, 2, 3])
    rolls = {}
    # we now go through the dice_notation parts and evaluate each argument
    for argument in message_parts:
        # we split the argument into the dice part and the modifier parts
        argument_parts = argument.split('.')
        # the first part of the argument is the dice part, we split it into the number of dice and the number of sides
        dice_parts = argument_parts[0].split('d')
        # we now get the number of dice and the number of sides
        number_of_dice = int(dice_parts[0])
        number_of_sides = int(dice_parts[1])
        # append the dice type to the dictionary if it doesn't exist
        if number_of_sides not in rolls:
            rolls[number_of_sides] = []
        # we now generate the rolls for this specific argument
        # we create a list to store the rolls
        rolls_list = []
        # we roll the dice and add them to the list
        for i in range(0, number_of_dice):
            rolls_list.append(random.randint(1, number_of_sides))
        
        # print("rolled " + str(rolls_list))

        # we can now split off the dice part from the argument parts
        argument_parts.pop(0)
        # we now apply the modifiers to the rolls
        # we go through each modifier
        for arg in range(0, len(argument_parts)):
            # print("applying modifier " + argument_parts[arg])
            # we split the modifier into the modifier and the value
            modifier_parts = argument_parts[arg].split('(')
            # we now get the modifier and the value
            modifier = modifier_parts[0]
            value = zim.get_first_number(modifier_parts[1])
            # if the modifier is droplowest
            if modifier == 'droplowest':
                # we sort the list and then drop the first x rolls
                rolls_list.sort()
                rolls_list = rolls_list[value:]
            # if the modifier is drophighest
            elif modifier == 'drophighest':
                # we sort the list and then drop the last x rolls
                rolls_list.sort()
                rolls_list = rolls_list[:-value]
            # if the modifier is reroll
            elif modifier == 'reroll':
                # we can go through each roll and reroll it if it's x
                for i in range(0, len(rolls_list)):
                    while rolls_list[i] == value:
                        rolls_list[i] = random.randint(1, number_of_sides)
                    # print that we rerolled a roll
                        # print('rerolled a ' + str(value) + ' into a ' + str(rolls_list[i]) + ' on a ' + str(number_of_sides) + ' sided die')
            # if the modifier is rerollonce
            elif modifier == 'rerollonce':
                # we can go through each roll and reroll it if it's x
                for i in range(0, len(rolls_list)):
                    if rolls_list[i] == value:
                        rolls_list[i] = random.randint(1, number_of_sides)
                    # print that we rerolled a roll
                        # print('rerolled a ' + str(value) + ' into a ' + str(rolls_list[i]) + ' on a ' + str(number_of_sides) + ' sided die')
            # if the modifier is keeplowest
            elif modifier == 'keeplowest':
                # we sort the list and then keep the first x rolls
                rolls_list.sort()
                rolls_list = rolls_list[:value]
            # if the modifier is keephighest
            elif modifier == 'keephighest':
                # we sort the list and then keep the last x rolls
                rolls_list.sort()
                rolls_list = rolls_list[-value:]
            
        # we now add the rolls to the corresponding list in the dictionary
        # print("after modifiers: " + str(rolls_list))
        rolls[number_of_sides].extend(rolls_list)
    # we now return the dictionary
    # print("full dictionary: " + str(rolls))
    return rolls

# takes a dice notation with modifiers and returns the sum of the rolls
def roll(dice_notation):
    # we use the usual ttrpg dice notation 
    # if there is a constant or die roll with + or - in front of it, we add or subtract that constant from the roll
    # if there is a constant or die roll with * or / in front of it, we multiply or divide that constant from the roll
    # if there is a die roll without a sign in front of it, we add that roll to the total
    # if there is a .drophighest(x) or .droplowest(x) after a die roll, we drop the highest or lowest x rolls of that roll
    # if there is a .reroll(x) after a die roll, we reroll any rolls that are equal to or lower than x until we get a roll higher than x
    # if there is a .rerollonce(x) after a die roll, we reroll any rolls that are equal or lower to x once
    # if there is a .keephighest(x) or .keeplowest(x) after a die roll, we keep the highest or lowest x rolls of that roll
    # if the only argument is adv or disadv, we roll 2d20 and keep the highest or lowest roll
    # if there is no argument, we roll 1d20

    # split the dice_notation into a list
    message_parts = dice_notation.split(' ')
    # first handle the case where there is no argument
    # print('arguments: ' + str(message_parts))
    if message_parts[0] == '':
        # print("defaulting to 1d20")
        # if there is no argument, we roll 1d20 and return the result
        return random.randint(1, 20)
    
    # if the only argument is adv or disadv, we roll 2d20 and keep the highest or lowest roll
    if message_parts[0] == 'adv' or message_parts[0] == 'disadv':
        # roll 2d20
        # print("rolling with " + message_parts[0] + "antage")
        roll1 = random.randint(1, 20)
        roll2 = random.randint(1, 20)
        # if the argument is adv, we keep the highest roll
        if message_parts[0] == 'adv':
            return max(roll1, roll2)
        # if the argument is disadv, we keep the lowest roll
        else:
            return min(roll1, roll2)
    
    # now we handle the case where there is any number of arguments
    # we go through each argument and handle it
    # we start with the total being 0
    total = 0
    # we go through each argument
    for argument in message_parts:
        operation = '+'
        # if there is a +, -, *, or / in front of the argument, we set the operation to that sign
        if argument[0] == '+' or argument[0] == '-' or argument[0] == '*' or argument[0] == '/':
            operation = argument[0]
            argument = argument[1:]
        # first we check if the argument is a constant
        if argument.isdigit():
            # if it is, we add or subtract that constant from the total
            if operation == '+':
                total += int(argument)
            elif operation == '-':
                total -= int(argument)
            elif operation == '*':
                total *= int(argument)
            elif operation == '/':
                total /= int(argument)
            # we skip the rest of the loop
            continue
        # we now remove the operator
        argument = argument.replace(operation, '')

        # we can now generate a dice set using rollset
        rolls = rollset(argument)
        # we get the sum of all entries in the dictionary
        rolls = sum([roll for rolls_for_one_dice in rolls.values() for roll in rolls_for_one_dice])
        
        # we now apply the sum of the rolls to the total with the operation
        if operation == '+':
            total += rolls
        elif operation == '-':
            total -= rolls
        elif operation == '*':
            total *= rolls
        elif operation == '/':
            total /= rolls
            
    # we return the total
    return total

# takes a dice notation with modifiers and a number of rolls
# returns the average roll
def average_roll_simulator(dice_notation, number_of_rolls):
    dice_roll = 0
    for i in range(number_of_rolls):
        dice_roll += roll(dice_notation)
    return dice_roll / number_of_rolls

# takes a dice notation with modifiers and a number of rolls
# returns a dictionary of the amount of times each roll was rolled
def roll_simulator(dice_notation, number_of_rolls):
    dice_rolls = {}
    for i in range(number_of_rolls):
        dice_roll = roll(dice_notation)
        if dice_roll in dice_rolls:
            dice_rolls[dice_roll] += 1
        else:
            dice_rolls[dice_roll] = 1
    return dice_rolls

# takes a dice notation with modifiers, a to hit modifier, an ac, a crit range, meaningful_crit and a number of rolls
# returns the average damage
def atk_simulator(dice_notation, to_hit_modifier, ac, crit_range, meaningful_crit, number_of_rolls):
    # dice_notation is the dice notation for the damage
    # to_hit_modifier is the to hit modifier
    # ac is the ac of the target
    # crit_range is the crit range of the weapon (eg 18-20)
    # meaningful_crit is a flag that determines if crits are meaningful (if they do more damage)
    # number_of_rolls is the number of rolls to simulate
    
    total = 0
    # we go through each roll
    for i in range(number_of_rolls):
        iscrit = False
        # we first roll to hit
        attack_roll = random.randint(1, 20)
        # if the attack roll is a crit, we roll damage twice if meaningful crits are disabled
        if attack_roll >= crit_range[0] and attack_roll <= crit_range[1]:
            iscrit = True
        # we now add the to hit modifier to the attack roll
        attack_roll += to_hit_modifier
        # if the attack roll is higher than the ac, we roll damage
        if (attack_roll >= ac):
            damage = roll(dice_notation)
            # if the attack roll is a crit but meaningful crits are disabled, we double the damage
            if (iscrit and not meaningful_crit):
                damage *= 2
            # if the attack roll is a crit and meaningful crits are enabled, we add the max damage of the roll to the damage
            elif (iscrit and meaningful_crit):
                damage += maxroll(dice_notation)
            # we add the damage to the total
            total += damage
    # we return the average damage
    return total / number_of_rolls

# takes a dice notatioon with modifiers
# returns the max roll with that dice notation
def maxroll(dice_notation):
    # we split the dice notation into a list
    message_parts = dice_notation.split(' ')
    # we start with the total being 0
    total = 0
    
    # there are some modifiers that we can ignore: reroll, rerollonce
    # for droplowest and drophighest, we can just subtract the max roll of the dice from the total
    # for keephighest and keeplowest, we can just add the max roll of the amt of dice to the total
    # we replace reroll and rerollonce with nothing
    