# 🍽️ Food Recommendation System using ChromaDB and RAG

A semantic food recommendation system built with **ChromaDB** (vector database) and **RAG** (Retrieval-Augmented Generation). The project is structured into three progressive parts — a CLI-based chatbot, an advanced search interface, and a RAG-powered conversational assistant.

---

## 📁 Project Structure

```
├── FoodDataSet.json              # Food dataset (JSON)
│
├── Part 1 - CLI/
│   ├── shard_functions.py        # Core ChromaDB & embedding utilities
│   ├── cli_functions.py          # CLI chatbot logic & display helpers
│   └── interactive_search.py    # Entry point for the CLI system
│
├── Part 2 - Advanced Search/
│   └── (coming soon)
│
├── Part 3 - RAG Chatbot/
│   └── (coming soon)
│
└── README.md
```

---

## 🔧 Prerequisites

- Python 3.8+
- pip

## 📦 Installation

```bash
pip install chromadb sentence-transformers numpy
```

---

## Part 1 — CLI Food Recommendation Chatbot

An interactive command-line chatbot that uses **ChromaDB** and **sentence-transformer embeddings** to perform semantic similarity search over a food dataset.

### Files

| File | Description |
|---|---|
| `shard_functions.py` | Core utilities — loads data, creates/populates ChromaDB collection, performs similarity & filtered search |
| `cli_functions.py` | CLI display logic — handles search output, related search suggestions, and the interactive chat loop |
| `interactive_search.py` | Entry point — initializes the database and launches the chatbot |

### How It Works

**1. Data Loading (`shard_functions.py` → `load_food_data`)**

Reads `FoodDataSet.json` and normalizes each food item to ensure required fields are present:
- `food_id`, `food_ingredients`, `food_description`, `cuisine_type`, `food_calories_per_serving`, `taste_profile`

**2. Collection Setup (`shard_functions.py` → `create_similarity_search_collection`)**

Creates a ChromaDB collection using the **`all-MiniLM-L6-v2`** sentence transformer model for generating semantic embeddings, with cosine similarity as the distance metric.

**3. Populating the Collection (`shard_functions.py` → `populate_similarity_collection`)**

Each food item is converted into a rich text document combining:
- Name, description, ingredients, cuisine type, cooking method, taste profile, health benefits, and nutritional factors

These documents are embedded and stored in ChromaDB along with metadata for filtering.

**4. Similarity Search (`shard_functions.py` → `perform_similarity_search`)**

Accepts a natural language query, embeds it, and retrieves the top-N most semantically similar food items. Returns results with a **similarity score** (1 - cosine distance).

**5. Filtered Search (`shard_functions.py` → `perform_filtered_similarity_search`)**

Extends similarity search with optional metadata filters:
- `cuisine_filter` — filter by cuisine type
- `max_calories` — filter by maximum calories per serving

**6. CLI Chatbot (`cli_functions.py` → `interactive_chat_bot`)**

An interactive REPL loop that:
- Accepts free-text food queries from the user
- Calls `handle_food_search` to display ranked results with match scores, cuisine, calories, and description
- Suggests related searches based on result cuisine types and average calories
- Supports `help` and `quit` commands

### Running Part 1

```bash
python interactive_search.py
```

### CLI Commands

| Command | Description |
|---|---|
| Any text | Search for food by name, ingredient, or description |
| `help` / `h` | Show help menu with example searches |
| `quit` / `exit` / `q` | Exit the chatbot |
| `Ctrl+C` | Emergency exit |

### Example Searches

```
Search for food: chocolate dessert
Search for food: Italian food
Search for food: low calorie
Search for food: baked goods with cheese
```

### Sample Output

```
🔍 Searching for 'chocolate dessert'...

✅ Found 5 recommendations:
============================================================

1. 🍽️  Chocolate Lava Cake
        📊 Match Score: 94.2%
        🏷️  Cuisine: American
        🔥 Calories: 420 per serving
        📝 Description: Rich chocolate cake with a gooey center...
   --------------------------------------------------
...
============================================================

💡 Related searches you might like:
        • Try 'American dishes' for more American options
        • Try 'hearty meal' for more substantial dishes
```

---

## Part 2 — Advanced Search

> 🚧 **Coming Soon**
>
> This section will cover advanced search capabilities including multi-filter queries, faceted search, hybrid search strategies, and an enhanced search interface built on top of the ChromaDB collection.

---

## Part 3 — RAG Chatbot

> 🚧 **Coming Soon**
>
> This section will integrate a Large Language Model (LLM) with the ChromaDB retrieval system to build a conversational RAG-based food recommendation chatbot — capable of understanding complex queries and generating natural language responses grounded in the food dataset.

---

## 🧠 Key Concepts

**ChromaDB** — An open-source vector database that stores and indexes embeddings for fast semantic similarity search.

**Sentence Transformers** — Neural network models that convert text into dense vector embeddings that capture semantic meaning. This project uses `all-MiniLM-L6-v2`.

**Cosine Similarity** — The distance metric used to compare query embeddings against stored food embeddings. A score closer to 1.0 indicates a stronger match.

**RAG (Retrieval-Augmented Generation)** — A technique that retrieves relevant documents from a knowledge base (ChromaDB) and feeds them as context to an LLM to generate accurate, grounded responses.

---

## 📄 License

This project is part of the IBM Skills Network lab — *Food Recommendation System using ChromaDB and RAG*.
