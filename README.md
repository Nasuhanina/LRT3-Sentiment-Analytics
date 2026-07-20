# LRT3 Sentiment Analysis

Sentiment analysis of public conversations on X (Twitter) about Malaysia's LRT3 Shah Alam Line.

## 📊 Project Overview

This project collects LRT3-related tweets from X, then runs sentiment analysis using the open-source **`bertweet-base-sentiment-analysis`** model to classify each tweet into sentiment categories. Results are displayed via an interactive dashboard.

## 🧠 Sentiment Model

Model: **[bertweet-base-sentiment-analysis](https://huggingface.co/finiteautomata/bertweet-base-sentiment-analysis)**
- Language model fine-tuned on tweets (BERTweet)
- Grouped into 3 categories: *Negative, Neutral, Positive*

## 🏗️ Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Flask (Python) — serves API for stats, word cloud, and charts |
| **Frontend** | React — interactive dashboard with stats, pie chart, and word cloud |
| **Analysis** | Hugging Face Transformers + bertweet-base-sentiment-analysis |

## 🚀 Getting Started

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Runs on `http://localhost:5000`

### Frontend

```bash
cd frontend
npm install
npm start
```

Runs on `http://localhost:3000` (API requests proxied to Flask)

## 📁 Data

Tweets stored in `lrt3-sentiment.csv` with the following structure:

| Column | Description |
|--------|-------------|
| `created_at` | Tweet timestamp |
| `lang` | Tweet language |
| `text` | Tweet content |
| `sentiment_label` | Sentiment label (5 classes) |
| `confidence` | Model confidence score |
| `sentiment_category` | Sentiment category (3 classes) |

## 📋 Results

Based on **232 tweets** analyzed:

| Sentiment | Count |
|-----------|-------|
| Neutral | 181 |
| Negative | 35 |
| Positive | 16 |
