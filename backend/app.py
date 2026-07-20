import os
import io
import base64
import pandas as pd
from collections import Counter
from flask import Flask, jsonify
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

app = Flask(__name__)
CORS(app)

CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lrt3-sentiment3.csv')
df = pd.read_csv(CSV_PATH)

STOPWORDS = set(stopwords.words('english'))
STOPWORDS.update(['https', 'http', 'co', 't', 'lrt3', 'will', 'get', 'via', 'amp', 'also', 'would', 'got', 'still', 'even', 'lrt3s'])

def get_sentiment_stats():
    label_counts = df['sentiment_label'].value_counts().to_dict()
    category_counts = df['sentiment_category'].value_counts().to_dict()
    total = len(df)
    avg_confidence = round(df['confidence'].mean(), 4)
    lang_dist = df['lang'].value_counts().to_dict()
    latest_date = df['created_at'].max()
    return {
        'total': total,
        'latest_date': latest_date,
        'label_counts': label_counts,
        'category_counts': category_counts,
        'avg_confidence': avg_confidence,
        'lang_dist': lang_dist
    }

def generate_wordcloud_base64(label_filter=None):
    texts = df['text']
    if label_filter:
        texts = df[df['sentiment_label'] == label_filter]['text']
    all_text = ' '.join(texts.dropna())
    wc = WordCloud(
        width=800, height=400,
        background_color='white',
        stopwords=STOPWORDS,
        max_words=100,
        collocations=False
    ).generate(all_text)

    frequencies = wc.words_
    if frequencies:
        max_freq = max(frequencies.values())
        min_freq = min(frequencies.values())
        def color_func(word, font_size, position, orientation, random_state=None, font_path=None):
            freq = frequencies.get(word, min_freq)
            ratio = (freq - min_freq) / (max_freq - min_freq) if max_freq > min_freq else 0.5
            if ratio > 0.5:
                t = (ratio - 0.5) * 2
                r = int(255 * t)
                g = 0
                b = int(255 * (1 - t))
            else:
                t = ratio * 2
                r = 0
                g = int(255 * (1 - t))
                b = int(255 * t)
            return f'rgb({r},{g},{b})'
        wc.recolor(color_func=color_func)

    buf = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

def generate_sentiment_chart_base64():
    labels = ['Negative', 'Neutral', 'Positive']
    order = {l: i for i, l in enumerate(labels)}
    counts = df['sentiment_label'].value_counts()
    vals = [counts.get(l, 0) for l in labels]
    colors = ['#d32f2f', '#f44336', '#9e9e9e']

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(labels, vals, color=colors)
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                str(v), ha='center', va='bottom', fontsize=11)
    ax.set_ylabel('Count')
    ax.set_title('Sentiment Distribution')
    ax.set_ylim(0, max(vals) * 1.15)
    plt.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

@app.route('/api/stats')
def stats():
    return jsonify(get_sentiment_stats())

@app.route('/api/wordcloud')
def wordcloud():
    img = generate_wordcloud_base64()
    return jsonify({'image': 'data:image/png;base64,' + img})

@app.route('/api/wordcloud/<label>')
def wordcloud_filtered(label):
    if label not in df['sentiment_label'].unique():
        return jsonify({'error': 'Invalid label'}), 400
    img = generate_wordcloud_base64(label)
    return jsonify({'image': 'data:image/png;base64,' + img})

@app.route('/api/chart/sentiment')
def sentiment_chart():
    img = generate_sentiment_chart_base64()
    return jsonify({'image': 'data:image/png;base64,' + img})

@app.route('/api/tweets')
def tweets():
    return jsonify(df.head(100).to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
