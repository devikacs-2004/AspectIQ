# AspectIQ 
### Product Review Intelligence System

> *Transforming 568,000 raw Amazon reviews into actionable business intelligence using NLP, Embeddings, and LLM-powered analysis.*

**[Live Demo](https://aspectiq-tjwughn8xcerccaiujmzjs.streamlit.app/)** | 📂 **[GitHub](https://github.com/devikacs-2004/AspectIQ)**

---

## The Problem

Amazon sellers and brand managers are drowning in customer reviews. A product with 50,000 reviews gets a **4.2 ⭐ average** — but that single number hides:
- *Which specific aspect* is driving complaints?
- *How severe* is each problem?
- *What exactly* are customers saying?

AspectIQ solves this by breaking reviews down by aspect and surfacing the real signal.

---

## What AspectIQ Does

Given a product's reviews, AspectIQ:

1. **Detects aspects** — identifies which of 4 key aspects (taste, packaging, delivery, price) each review mentions
2. **Measures sentiment** — positive, negative, or neutral per aspect
3. **Summarizes complaints** — uses LLM to distill hundreds of complaints into 3 actionable bullet points
4. **Quantifies business impact** — estimates revenue recovery from fixing top complaints

---

## Technical Architecture
Raw Reviews (568k)
↓
Text Preprocessing (regex, lowercasing, punctuation removal)
↓
Aspect Detection (Sentence Transformers + Cosine Similarity)
↓
Sentiment Analysis (VADER)
↓
LLM Summarization (Groq — LLaMA 3)
↓
Interactive Dashboard (Streamlit + Plotly)

---

##  ML Stack & Key Concepts

| Component | Technology | Why |
|---|---|---|
| Text Embeddings | `sentence-transformers/all-MiniLM-L6-v2` | Captures semantic meaning, not just keywords |
| Similarity Matching | Cosine Similarity | Measures angle between embedding vectors |
| Sentiment Analysis | VADER (NLTK) | Fast, accurate for review text |
| LLM Summarization | Groq API (LLaMA 3.1) | Distills complaints into actionable insights |
| Dashboard | Streamlit + Plotly | Interactive, real-time visualizations |

---

## Key Results (10,000 reviews sample)

| Aspect | Mentions | Negative Rate | Top Complaint |
|---|---|---|---|
| Taste | 7,491 | 6.2% | Flavor not matching description |
| Packaging | 985 | **10.5%** | Items arriving damaged/crushed |
| Price | 415 | **13.0%** | Overpriced vs in-store alternatives |
| Delivery | 361 | 8.9% | Long shipping times |

> **Key Insight:** Despite fewer mentions, Packaging and Price have 2x the complaint rate of Taste — making them higher-priority improvement areas for brand owners.

---

## Dashboard Features

- **Overview Page** — Total reviews analyzed, aspect distribution, sentiment breakdown
- **Aspect Intelligence** — Per-aspect sentiment health score (gauge), breakdown charts, AI-powered complaint analysis
- **Business Impact Calculator** — Live ROI estimation: "If you fix X% of packaging complaints, you recover $Y/month"

---

##  Honest Limitations

- VADER misclassifies sarcastic/ironic language (~10-15% of edge cases)
- Aspect keywords may miss highly domain-specific terminology
- Business impact estimates are directional, not precise — based on published research on review-to-revenue correlations

---

## Future Improvements

- [ ] Custom dataset upload (v2 — in progress)
- [ ] Transformer-based sentiment model (DistilBERT) to replace VADER
- [ ] Time-series analysis — how sentiment changes over time
- [ ] Product comparison mode

---

##  Local Setup

```bash
git clone https://github.com/devikacs-2004/AspectIQ.git
cd AspectIQ
pip install -r requirements.txt
streamlit run app.py
```
---

## 👩‍💻 Built By

**Devika CS** — Aspiring Data Scientist | BTech CSE 2026
-  [Portfolio](https://devikacs.vercel.app)
-  [LinkedIn](www.linkedin.com/in/devika-cs-594511286)
-  Based in Sharjah, UAE
