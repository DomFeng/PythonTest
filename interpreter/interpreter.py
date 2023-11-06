import interpreter

interpreter.model = "gpt-3.5-turbo"
# # Paste your OpenAI API key below.
interpreter.api_key = "sess-4YThLTfF2KP5dLWum9AZAsgc9cxx5VGlRN15HZql"
# interpreter.local = True 

# message = "绘制AAPL和META的归一化股价图"

# for chunk in interpreter.chat(message, display=False, stream=True):
#   print(chunk)

interpreter.chat("Please print hello world.")
# interpreter.auto_run = True