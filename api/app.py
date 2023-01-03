from flask import Flask, request, render_template

from bot import get_response

app = Flask(__name__)

convo = []


@app.route('/', methods=['GET', 'POST'])
def chat():
    # Probably not the best way to do this, but it works
    global convo

    if request.method == 'POST':
        question = 'You: ' + request.form['question']
        answer = 'Bot: ' + str(get_response(question))

        convo.append(question)
        convo.append(answer)

        return render_template('form.html', answer=convo)

    return render_template('form.html')
