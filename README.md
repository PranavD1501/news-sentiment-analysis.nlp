# news-sentiment-analysis.nlp

# 📰 News Sentiment Analysis using Sentence Transformers

This project builds a full pipeline for financial news sentiment analysis using state-of-the-art NLP techniques. We scrape news data from **X (Twitter)** and **Yahoo Finance**, generate **sentence embeddings** using **Sentence Transformers**, and classify them using a custom **sentiment classifier**.

---

## 🚀 Features

- 🔍 Scrapes real-time headlines from Yahoo Finance and X (formerly Twitter)
- ✨ Uses Sentence Transformers (BERT-based models) for contextual embeddings
- 🎯 Trains a classifier (e.g., Logistic Regression, SVM, or fine-tuned BERT) on labeled data
- 📈 Visualizes sentiment distribution and trends over time
- 🗂️ Modular pipeline with reusable components

---

## 🧠 Tech Stack

- **Language**: Python
- **Libraries**:
  - `sentence-transformers`
  - `scikit-learn`
  - `pandas`, `numpy`
  - `matplotlib`, `seaborn`
  - `beautifulsoup4`, `requests`, `snscrape`
- **Model**: Sentence-BERT (e.g., `all-MiniLM-L6-v2`)
- **Sources**: Yahoo Finance, X/Twitter (via `snscrape`)

---

## 📁 Project Structure




