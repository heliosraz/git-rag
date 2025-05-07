import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
import chat
import processing

script_dir = os.path.dirname(os.path.abspath(__file__))
try:
    os.makedirs(os.path.join(script_dir, "data"))
    processing.main()
except OSError:
    print("Processing Happened Already...")

chat = chat.ChatLLM()
chat.run()