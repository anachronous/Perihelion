# various templates for the alpaca llm

# intent is a instruction to the llm (the standard llama template)
def instruction(prompt):
    return "You are a helpful, friendly and obedient AI. Follow the following instruction as exactly as you can: " + prompt