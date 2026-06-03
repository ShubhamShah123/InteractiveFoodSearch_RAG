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
│   ├── advanced_search_functions.py  # All advanced search modes & display logic
│   └── advanced_search.py            # Entry point for the advanced search system
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

An interactive menu-driven search system that extends Part 1 with **cuisine filtering**, **calorie filtering**, **combined filters**, and a **demo mode** — all built on top of the same ChromaDB collection from `shard_functions.py`.

### Files

| File | Description |
|---|---|
| `advanced_search_functions.py` | All search modes, display logic, demo mode, and the interactive menu loop |
| `advanced_search.py` | Entry point — loads data, sets up the collection, and launches the advanced search interface |

### How It Works

**1. Entry Point (`advanced_search.py` → `main`)**

Loads the food dataset using `load_food_data`, creates a new ChromaDB collection named `advanced_food_search`, populates it via `populate_similarity_collection`, then hands control to `interactive_advanced_search`.

**2. Result Display (`advanced_search_functions.py` → `display_search_results`)**

A shared display utility used by all search modes. Accepts a `showDetails` flag:
- `True` — shows full details: name, similarity score, cuisine, calories, and description
- `False` — shows names only (used in demo mode for a compact summary view)

**3. Search Modes (`advanced_search_functions.py`)**

| Mode | Function | Description |
|---|---|---|
| Basic Search | `perform_basic_search` | Free-text similarity search, returns top 5 results |
| Cuisine Filter | `perform_cuisine_filtered_search` | Picks a cuisine from a predefined list, then searches within it |
| Calorie Filter | `perform_calorie_filtered_search` | Searches with an optional maximum calorie cap |
| Combined Filter | `perform_combined_filtered_search` | Applies both cuisine and calorie filters simultaneously |
| Demo Mode | `demo_mode` | Runs 3 predefined demonstrations step-by-step with Enter to continue |
| Help | `advanced_help` | Prints tips and descriptions for all search types |

**4. Interactive Menu (`advanced_search_functions.py` → `interactive_advanced_search`)**

A numbered menu loop (options 1–7) that maps each choice to its corresponding function. Handles invalid input and `KeyboardInterrupt` gracefully.

**5. Demo Mode (`advanced_search_functions.py` → `demo_mode`)**

Runs three predefined search scenarios automatically to showcase the filtering system:

| Demo | Query | Filters |
|---|---|---|
| Italian Cuisine Search | `creamy pasta` | Cuisine: Italian |
| Low-Calorie Healthy Options | `healthy meal` | Max Calories: 300 |
| Asian Light Dishes | `light fresh meal` | Cuisine: Japanese, Max Calories: 250 |

### Running Part 2

```bash
python advanced_search.py
```

### Menu Options

```
========================================
ADVANCED SEARCH WITH FILTERS
========================================
    1: Basic Similarity Search
    2: Cuisine-Filtered Search
    3: Calorie-Filtered Search
    4: Combined Filters Search
    5: Demo Mode
    6: Help
    7: Exit
```

### Supported Cuisines (for Cuisine Filter)

`Italian`, `Thai`, `Mexican`, `Indian`, `Japanese`, `French`, `Mediterranean`, `American`, `Health Food`, `Dessert`

### Sample Output

```
[+] Performing cuisine filtered search ...
Available Cuisines:
    1. Italian
    2. Thai
    ...

Enter the search query: creamy pasta
Enter the cuisine number or name: 1

    [X] Searching for 'creamy pasta' in Italian cuisine...

#### Cuisine-Filtered Results - Italian ####

1. Fettuccine Alfredo
> Similarity Score: 91.3%
> Cuisine: Italian
> Calories: 520
> Description: Creamy pasta with butter and parmesan...
##########
```

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
