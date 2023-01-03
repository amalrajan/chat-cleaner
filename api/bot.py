import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

prompt_custom = ''


def get_response(question):
    global prompt_custom
    question = 'You: ' + question
    prompt_custom += question + '\n' + '<AI>:'

    response = openai.Completion.create(
        model='<Model>',
        prompt=prompt_custom,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.51,
        stop=['You:', '<AI>:']
    )

    bot_reply = response.choices[0].text
    bot_reply = bot_reply.split('\n')[0]
    bot_reply = bot_reply.replace('  ', '.\n')
    prompt_custom += bot_reply + '\n'

    print('You: ' + question)
    print('Bot: ' + bot_reply)
    print()

    return bot_reply
