'''from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)

def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity

    if sentiment_score > 0:
        return "POSITIVE"
    elif sentiment_score < 0:
        return "NEGATIVE"
    else:
        return "NEUTRAL"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        user_input = request.form['user_input']
        sentiment = analyze_sentiment(user_input)
        return render_template('result.html', sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True)'''

from flask import Flask, render_template, request, redirect, url_for
from textblob import TextBlob
import pandas as pd

app = Flask(__name__)

def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity

    if sentiment_score > 0:
        return "POSITIVE"
    elif sentiment_score < 0:
        return "NEGATIVE"
    else:
        return "NEUTRAL"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('index'))

        file = request.files['file']

        if file.filename == '':
            return redirect(url_for('index'))

        if file:
            # Read the Excel file without headers
            df = pd.read_excel(file, header=None)

            # Perform sentiment analysis on each sentence in the dataset
            sentiments = []
            for sentence in df[0]:
                sentiment = analyze_sentiment(sentence)
                sentiments.append(sentiment)

            # Combine the original dataset with the sentiment analysis results
            df['Sentiment'] = sentiments

            # Save the result to a new Excel file (you can also return it as a response)
            result_file_path = 'static/result.xlsx'
            df.to_excel(result_file_path, index=False, header=False)

            # Pass the DataFrame to the template
            return render_template('result.html', df=df, result_file=result_file_path)

if __name__ == '__main__':
    app.run(debug=True)
