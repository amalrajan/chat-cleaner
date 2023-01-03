# Build your own GPT-3 chatbot

Here's how you can create your own GPT-3 based chatbot from WhatsApp chats.

## Instructions

1. Export WhatsApp chat between you and another person (or multiple people). For better accuracy, you'd need >10k lines.
2. Paste your chat in api/preprocess/chat.txt and run clean.py. This would generate a chat.jsonl file. 
3. Get an OpenAI API key and set it as an environment variable.
4. `pip install --upgrade openai; openai api fine_tunes.create -t api/preprocess/chat.jsonl -m curie`. As a side note, I would go with davinci instead of curie if I could.

Keep polling for the status of fine-tuning using this cURL:
```
curl --location --request GET 'https://api.openai.com/v1/fine-tunes' \
--header 'Authorization: Bearer <bearer>'
```

Once it's done, you'd see `"status": "succeeded"`

5. Replace `<Model>` in bot.py with the actual model ID
6. Run the script or host the wsgi server somewhere nice!

`gunicorn api.app:app`


## Wishlist
- I want to use websockets
- A small script to include contextual prompt

