import pathlib
import textwrap
import google.generativeai as genai

genai.configure(api_key="AIzaSyA144dpQmD-S9jCvJhXn2ih8cx2l_i89FQ")

model = genai.GenerativeModel('gemini-pro')

chat = model.start_chat(history=[])
chat

response = chat.send_message("Que es react native", stream=True)
for chunk in response:
  print(chunk.text)
print("*/*"*80)

response = chat.send_message("comprendo, y que proyectos puedo hacer.", stream=True)

#response = model.generate_content("What is the meaning of life?")

#response = model.generate_content("deseo conocer proyectos en base a lo que te pregunte anteriormente", stream=True)
for chunk in response:
  print(chunk.text)