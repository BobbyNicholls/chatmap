from flask import Flask, render_template, request


from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

print("starting...")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if device == "cpu":
    print("GPU not found")
    quit()

# "tiiuae/falcon-7b-instruct" doesnt require access, there is also a 40b version.
# alternatives: "OpenAssistant/oasst-sft-6-llama-30b", "meta-llama/Llama-2-13b-chat-hf"
model_to_use = "meta-llama/Llama-2-7b-chat-hf"
print(f"Loading {model_to_use} on {device}")

# Try to pull the model from the cache, if that fails download the model and cache it
cache_location = f"model_cache/{test_model_to_use}"
try:
    model = AutoModelForCausalLM.from_pretrained(cache_location, device_map="auto")
    tokenizer = AutoTokenizer.from_pretrained(cache_location)
except:
    tokenizer = AutoTokenizer.from_pretrained(model_to_use, cache_dir=cache_location)
    model = AutoModelForCausalLM.from_pretrained(
        model_to_use,
        cache_dir=cache_location,
    )
    tokenizer.save_pretrained(cache_location)
    model.save_pretrained(cache_location)

tokenizer.pad_token = tokenizer.eos_token
print("LLM Loaded")

print("Launching app")
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    print("Starting chat")
    msg = request.form["msg"]
    text_input = msg
    output_text = get_chat_response(text_input)
    return output_text


def get_chat_response(text):
    chat_history_ids = []  # TODO: Fix this
    print("Getting chat response")
    new_user_input = tokenizer(
        str(text) + tokenizer.eos_token,
        return_tensors="pt",
        padding=True,
        truncation=True,
    )
    new_user_input_ids = new_user_input["input_ids"].to(device)
    attention_mask = new_user_input["attention_mask"].to(device)

    try:
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
        attention_mask = torch.cat([attention_mask, attention_mask], dim=-1)
    except:
        bot_input_ids = new_user_input_ids

    print(f"Bot input IDs: {bot_input_ids}")
    chat_history_ids = model.generate(
        bot_input_ids,
        attention_mask=attention_mask,
        max_length=1000,
        pad_token_id=tokenizer.pad_token_id,
    )
    print(tokenizer.decode(bot_input_ids[0], skip_special_tokens=True).strip())
    print(tokenizer.decode(chat_history_ids[0], skip_special_tokens=True).strip())

    return tokenizer.decode(
        chat_history_ids[:, bot_input_ids.shape[-1] :][0], skip_special_tokens=True
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
