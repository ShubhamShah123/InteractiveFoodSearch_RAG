# 🍽️ Food Recommendation System using ChromaDB and RAG

A hands-on project that builds an intelligent food recommendation chatbot using **ChromaDB** as a vector database and **Retrieval-Augmented Generation (RAG)** to deliver personalized, context-aware food suggestions.

---

## 📌 Overview

This project demonstrates how to combine vector similarity search with large language models (LLMs) to create a smart recommendation system. Instead of relying solely on an LLM's training data, we store food-related information in ChromaDB and retrieve the most relevant entries before generating a response — making recommendations more accurate and grounded.

---

## 🧠 Key Concepts

| Concept | Description |
|---|---|
| **ChromaDB** | An open-source vector database for storing and querying embeddings |
| **Embeddings** | Numerical vector representations of text that capture semantic meaning |
| **RAG** | Retrieval-Augmented Generation — enhancing LLM responses with retrieved context |
| **Similarity Search** | Finding the most semantically similar items in a vector store |

---

## 🛠️ Tech Stack

- **Python**
- **ChromaDB** — vector database
- **Sentence Transformers / OpenAI Embeddings** — for generating text embeddings
- **LLM (e.g., OpenAI GPT / IBM Watsonx)** — for generating recommendations
- **Theia IDE** (Skills Network browser-based environment)

---

## 🚀 How It Works

```
User Query
    │
    ▼
Generate Embedding (query → vector)
    │
    ▼
ChromaDB Similarity Search
    │
    ▼
Retrieve Top-K Relevant Food Items
    │
    ▼
Pass Context + Query to LLM
    │
    ▼
Generate Personalized Food Recommendation
```

1. **Ingest Data** — Food items (dishes, recipes, cuisines) are embedded and stored in ChromaDB.
2. **Query** — A user asks for a recommendation (e.g., *"suggest a light Italian dinner"*).
3. **Retrieve** — ChromaDB finds the most semantically similar food items.
4. **Generate** — The LLM uses the retrieved context to craft a tailored recommendation.

---

## 📂 Project Structure

```
food-recommendation-rag/
│
├── data/
│   └── food_data.json          # Food items dataset
│
├── src/
│   ├── ingest.py               # Embed and load data into ChromaDB
│   ├── retrieve.py             # Query ChromaDB for similar items
│   └── recommend.py            # RAG pipeline — retrieve + generate
│
├── chroma_db/                  # Persisted ChromaDB vector store
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

```bash
# Clone the repository
git clone https://github.com/your-username/food-recommendation-rag.git
cd food-recommendation-rag

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt** includes:
```
chromadb
sentence-transformers
openai        # or ibm-watsonx-ai
```

---

## 📖 Usage

### 1. Ingest food data into ChromaDB
```bash
python src/ingest.py
```

### 2. Run the recommendation system
```bash
python src/recommend.py --query "I want something spicy and vegetarian"
```

### 3. Example output
```
Query: "I want something spicy and vegetarian"

Retrieved Items:
  - Chana Masala (Indian, Spicy, Vegan)
  - Tofu Pad Thai (Thai, Medium Spice, Vegetarian)
  - Shakshuka (Middle Eastern, Spicy, Vegetarian)

Recommendation:
  Based on your preference for spicy vegetarian food, I'd suggest Chana Masala —
  a hearty Indian chickpea curry bursting with bold spices. If you prefer something
  lighter, Shakshuka is a wonderful egg-based dish with a rich, spicy tomato sauce.
```

---

## 🎓 Learning Objectives

By completing this project, you will:

- Understand how **vector databases** work and why they're useful for AI applications
- Learn to generate and store **text embeddings**
- Build a complete **RAG pipeline** from scratch
- See how retrieval improves LLM output quality over pure generation

---

## 📄 License

This project is part of the IBM Skills Network curriculum and is intended for educational purposes.

---

## 🤝 Acknowledgements

- [ChromaDB](https://www.trychroma.com/)
- [IBM Skills Network](https://skills.network/)
- [Sentence Transformers](https://www.sbert.net/)
