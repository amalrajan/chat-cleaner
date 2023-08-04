<h1 align="center">Chat Cleaner</h1>

<p align="center">
  A script for pre-processing WhatsApp exported chats, enhancing their quality and structure to optimize training for GPT-3 models.
</p>

## Before you start

This utility is used to pre-process WhatsApp chats for training GPT-3 models.<br />
The source code also contains a Flask app that can be used to host a chatbot that uses the fine-tuned model.

## Instructions

1. Export WhatsApp chat between you and another person (or multiple people).
2. Paste your chat in api/preprocess/chat.txt and run clean.py. This would generate a chat.jsonl file. 
3. Get an OpenAI API key and set it as an environment variable.
4. `pip install --upgrade openai; openai api fine_tunes.create -t api/preprocess/chat.jsonl -m curie`. As a side note, I would go with davinci instead of curie if I could.
5. Keep polling for the status of fine-tuning using this cURL:
    ```
    curl --location --request GET 'https://api.openai.com/v1/fine-tunes' \
    --header 'Authorization: Bearer <bearer>'
    ```

6. Once it's done, you'd see `"status": "succeeded"`

7. Replace `<Model>` in bot.py with the actual model ID
8. Run the script or host the wsgi server somewhere nice!

    `gunicorn api.app:app`


## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
