import os

from flask import Flask, render_template, request
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

from utils.chat import ChatSession

print("starting...")

device = "cpu"
test_model_to_use = "Qwen/Qwen2.5-0.5B"
print(f"Loading {test_model_to_use} on {device}")

# Try to pull the model from the cache, if that fails download the model and cache it
cache_location = f"model_cache/{test_model_to_use}"
tokenizer = AutoTokenizer.from_pretrained(test_model_to_use, cache_dir=cache_location)
model = AutoModelForCausalLM.from_pretrained(
    test_model_to_use,
    cache_dir=cache_location,
)
if not os.path.isdir(cache_location):
    tokenizer.save_pretrained(cache_location)
    model.save_pretrained(cache_location)

tokenizer.pad_token = tokenizer.eos_token
print("LLM Loaded")

print("Launching app")
app = Flask(__name__)

chat_session = ChatSession(tokenizer, model)

@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    message = request.form["msg"]
    print(f"Getting chat response using this message: {message}")
    output_text = chat_session.get_chat_response(message)
    return output_text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
