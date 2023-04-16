### Math module for discord bot
import math
import scipy as sci

def uspensky_formula(total, num_dice, sides):
    prob = 0
    for k in range(0, int((total - num_dice) / sides) + 1):
        prob += ((-1)**k) * (math.comb(num_dice, k) * math.comb((total - k * sides - 1), num_dice - 1))
    prob = prob / (sides**num_dice)
    return prob

# gets the first number of a string
# for example: get_first_number('1d20') returns 1
# for example: get_first_number('2d4 + 1d6') returns 2¨
# for example: get_first_number("20d10") returns 20
def get_first_number(string):
    for char in string:
        if char.isdigit():
            number = char
            for i in string[len(number):]:
                if i.isdigit():
                    number += i
                else:
                    return int(number)
    return None
# thx chatgpt for this one my brain is fried