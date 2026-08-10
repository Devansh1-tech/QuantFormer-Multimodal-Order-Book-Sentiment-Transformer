# 📈 QuantFormer: Multi-modal Order Book & Sentiment Transformer

> AI-powered short-term stock price prediction using **Level-2 Order Book**, **Financial News Sentiment**, **FinBERT**, and **Temporal Fusion Transformer (TFT)**.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red)
![React](https://img.shields.io/badge/React-Frontend-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# 📖 Overview

QuantFormer is an AI-powered decision support system that predicts **short-term stock price movements** by combining **Level-2 (L2) Limit Order Book data** with **Financial News Sentiment**.

Unlike traditional forecasting models that rely only on historical prices, QuantFormer uses a **multi-modal deep learning architecture** that understands both structured financial market data and unstructured financial news simultaneously.

The system predicts the **next 5-minute stock movement** and provides actionable trading insights through an interactive dashboard.

---

# ❗ Problem Statement

Predicting short-term stock movements is a challenging task because stock prices are influenced by both:

- Live market order flow (Buy/Sell Orders)
- Financial news and market sentiment

Traditional forecasting models such as **ARIMA** and **LSTM** mainly analyze historical price data and cannot effectively combine structured order book information with unstructured financial news.

As a result, they often fail to capture sudden market movements caused by breaking news.

---

# 💡 Proposed Solution

QuantFormer solves this problem by integrating:

- 📊 Level-2 Order Book Analysis
- 📰 Financial News Sentiment
- 🤖 FinBERT
- 🧠 Temporal Fusion Transformer (TFT)

The system processes both data sources simultaneously and predicts the **future stock price movement** within the next **5 minutes**.

---

# 🚀 Features

- 📈 Next 5-minute Stock Price Prediction
- 📊 Level-2 Order Book Visualization
- 📰 Financial News Analysis
- 😊 Sentiment Analysis using FinBERT
- 🤖 Temporal Fusion Transformer
- 📉 Buy / Sell / Hold Recommendation
- 🎯 Prediction Confidence Score
- 📊 Interactive Candlestick Charts
- 🔥 Order Book Heatmap
- 📈 Prediction Overlay
- 📋 Explainable AI Dashboard

---

# 🏗️ Project Architecture

```
                Financial News
                       │
                       ▼
                   FinBERT
                       │
              Sentiment Score
                       │
                       ▼
Level-2 Order Book ─────────────┐
                                │
                                ▼
               Temporal Fusion Transformer
                                │
                                ▼
                  Future Price Prediction
                                │
                                ▼
                 Buy / Sell / Hold Signal
                                │
                                ▼
                 React Dashboard (UI)
```

---

# 📂 Dataset

## 1. FI-2010 Limit Order Book Dataset

Purpose

- Level-2 Order Book Data
- Time-Series Forecasting
- Price Movement Prediction

---

## 2. Financial PhraseBank

Purpose

- Financial News
- Sentiment Analysis
- FinBERT Input

---

## 3. Yahoo Finance (yfinance)

Purpose

- Historical Stock Prices
- Candlestick Charts
- Dashboard Visualization

---

# 🤖 AI Models

## FinBERT

Input

- Financial News Headlines

Output

- Positive
- Neutral
- Negative Sentiment

---

## Temporal Fusion Transformer (TFT)

Input

- Order Book Features
- News Sentiment

Output

- Next 5-minute Stock Price Prediction

---

# 🛠️ Tech Stack

## Frontend

- React.js
- TypeScript
- Tailwind CSS
- Plotly.js
- TradingView Lightweight Charts

## Backend

- FastAPI
- Python

## Machine Learning

- PyTorch
- Hugging Face Transformers
- FinBERT
- Temporal Fusion Transformer

## Data Processing

- Pandas
- NumPy
- Scikit-learn

## Visualization

- Plotly
- TradingView Charts
- Matplotlib

---

# 📁 Project Structure

```
QuantFormer/

│── backend/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── utils/
│   └── main.py
│
│── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── charts/
│   └── App.tsx
│
│── datasets/
│   ├── FI-2010/
│   ├── FinancialPhraseBank/
│   └── processed/
│
│── notebooks/
│
│── models/
│
│── docs/
│
│── requirements.txt
│
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/QuantFormer.git
```

Move into project

```bash
cd QuantFormer
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run backend

```bash
uvicorn main:app --reload
```

Run frontend

```bash
npm install
npm run dev
```

---

# 📊 Expected Output

The system predicts

- Future Stock Price
- Price Movement (Up / Down)
- Buy / Sell / Hold Recommendation
- Confidence Score
- News Sentiment
- Order Book Visualization

---

# 🎯 Future Improvements

- Live Market Data Integration
- Real-time Reuters News Feed
- Portfolio Optimization
- Risk Management Module
- Reinforcement Learning Agent
- Multi-stock Prediction
- Cloud Deployment

---

# 📚 References

- FI-2010 Limit Order Book Dataset
- Financial PhraseBank
- FinBERT
- Temporal Fusion Transformer
- Yahoo Finance API

---

# 👨‍💻 Team

**Internship Project**

**Project Name:** QuantFormer

**Domain:** FinTech • Deep Learning • NLP • Time-Series Forecasting

---

## ⭐ If you found this project useful, don't forget to star the repository.
