class ChatSession:
    def __init__(self, tokenizer, model):
        self.text_input = "For the duration of this conversation act like a bird. "
        self.tokenizer = tokenizer
        self.model = model

    def get_chat_response(self, text):
        self.text_input += (text + self.tokenizer.eos_token)
        tokenised_text = self.tokenizer(
            self.text_input,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )
        bot_input_ids = tokenised_text["input_ids"]
        attention_mask = tokenised_text["attention_mask"]

        print(f"Bot input IDs: {bot_input_ids}")
        bot_output_ids = self.model.generate(
            bot_input_ids,
            attention_mask=attention_mask,
            max_length=10,
            pad_token_id=self.tokenizer.pad_token_id,
        )
        output_text = self.tokenizer.decode(
            bot_output_ids[:, bot_input_ids.shape[-1] :][0], skip_special_tokens=True
        )
        print(f"Attention mask: {attention_mask}")
        print(f"Input: {self.tokenizer.decode(bot_input_ids[0], skip_special_tokens=True).strip()}")
        print(f"Output: {output_text}")

        self.text_input += (output_text + self.tokenizer.eos_token)
        return output_text