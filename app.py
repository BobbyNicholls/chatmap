from flask import Flask, render_template, request, jsonify


from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


# tokenizer = AutoTokenizer.from_pretrained("OpenAssistant/oasst-sft-6-llama-30b")
# model = AutoModelForCausalLM.from_pretrained("OpenAssistant/oasst-sft-6-llama-30b")

# Doesnt require access, there is also a 40b version
tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct")
model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-7b-instruct")
chat_history_ids = []

# Use when my access is approved
# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf")
# model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-13b-chat-hf")


tokenizer.pad_token = tokenizer.eos_token

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    text_input = msg
    output_text = get_chat_response(text_input)
    return output_text


def get_chat_response(text):
    chat_history_ids = []
    # Let's chat for 5 lines
    for step in range(5):
        print(f"Step: {step}")
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input = tokenizer(
            str(text) + tokenizer.eos_token,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )
        new_user_input_ids = new_user_input['input_ids']
        attention_mask = new_user_input["attention_mask"]

        if step > 0:
            bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
            attention_mask = torch.cat(
                [attention_mask, attention_mask], dim=-1
            )  # Extend the attention mask
        else:
            bot_input_ids = new_user_input_ids

        print(f"Bot input IDs: {bot_input_ids}")
        chat_history_ids = model.generate(
            bot_input_ids,
            attention_mask=attention_mask,
            max_length=50,
            pad_token_id=tokenizer.pad_token_id,
        )
        # generated a response while limiting the total chat history to 1000 tokens,
        # chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        print(tokenizer.decode(
            bot_input_ids[0], skip_special_tokens=True
        ).strip())
        print(tokenizer.decode(
            chat_history_ids[0], skip_special_tokens=True
        ).strip())

        return tokenizer.decode(
            chat_history_ids[:, bot_input_ids.shape[-1] :][0], skip_special_tokens=True
        )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
