import gradio as gr
import os
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_llm_response(message):
    response = chat.send_message(message)
    print(response)
    return response.text

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

base_info = """
You are OrderBot, an automated service to collect orders for a Burger Raja Restaurant. \
You first greet the customer, then collects the order, \
and then asks if its a pickup or delivery. \
Please do not use your own knowladge, stick within the given context only. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else.
"""
delivery_info = """If its a delivery, you ask for an address. \
Finally you collect the payment. \
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu. \
You respond in a short, very conversational friendly style. \
The menu includes"""
burger_type = """
peri peri burger for 149 Rs \
KFC burger for 139 Rs \
overloaded burger for 145 Rs\
Afghani burger for 149 Rs \
mumbai burger for 129 Rs \
"""
fries = "60 Rs 45 Rs"
toppings = """
greek salad 30 Rs \
lettuce 15 Rs  \
tomato 15 Rs  \
onion 15 Rs  \
pickles 15 Rs  \
mushrooms 15 Rs  \
extra cheese 20 Rs  \
sausage 30 Rs  \
canadian bacon 35 Rs  \
AI sauce 15 Rs  \
peppers 10 Rs \
AI masala 30 Rs \
"""
# define drinks
drinks = """
coke 60 Rs, 45 Rs, 30 Rs \
sprite 60 Rs, 45 Rs, 30 Rs \
bottled water 50 Rs
"""
#define ice cream
icecream ='''
vanilla 60 Rs, 45 Rs, 30 Rs \
chocolate 60 Rs, 45 Rs, 30 Rs \
strawberry 60 Rs, 45 Rs, 30 Rs
'''
context = [f"""
{base_info} \
{delivery_info} \
{burger_type} \
fries: {fries} \
Toppings: {toppings} \
Drinks: {drinks} \
Ice-Cream: {icecream}\
"""]  # accumulate messages

# create welcome message
context.append("")
response = get_llm_response(context)

# define communication function
def bot(message, history):
  prompt = message
  context.append(prompt)
  response = get_llm_response(context)
  context.append(response)
  return response

# create gradio instance
demo = gr.ChatInterface(fn=bot, examples=["🍔🍟🥤", "overloaded burger", "afghani burger", "Toppings: extra cheese/ AI sauce", "Drinks: coke/sprite/bottled water", "Ice-cream: Vanilla / chocolate/strawberry"], title=response)
demo.launch(debug=True, share=True)
