import chromadb
from chromadb.utils import embedding_functions
import json
import re
import numpy as np
from typing import List, Dict, Any, Optional

# Initialize ChromaDB client
client = chromadb.Client()


def load_food_data(file_path: str) -> List[Dict]:
	"""
	Load food data from JSON file
	"""
	print("---- load food data ----")
	try:
		with open(file_path, 'r') as file:
			food_data = json.load(file)

		# Normalizing food id to string
		for i, item in enumerate(food_data):
			item['food_id'] = str(i+1) if 'food_id' not in item else str(item['food_id'])
		
		# Ensuring the required fields.
		if 'food_ingredients' not in item:
			item['food_ingredients'] = []
		if 'food_description' not in item:
			item['food_description'] = ''
		if 'cuisine_type' not in item:
			item['cuisine_type'] = 'Unknown'
		if 'food_calories_per_serving' not in item:
			item['food_calories_per_serving'] = 0

		# Extracting taste features from nested food_featurse if available.
		if 'food_features' in item and isinstance(item['food_features'], dict):
			taste_features = []
			for key, val in item['food_features'].items():
				if val:
					taste_features.append(str(val))
				item['taste_profile'] = ', '.join(taste_features)
		else:
			item['taste_profile'] = ''
		print(f"Successfully loaded {len(food_data)} items from {file_path}")
		return food_data
	except Exception as error:
		print(f"Error loading food data: {error}")
		return []
    
def create_similarity_search_collection(collection_name: str, collection_metadata: dict = None):
	"""
	Creating the chromadb collection and sentence transformer embeddings
	"""
	print("---- create_similarity_search_collection ----")
	try:
		client.delete_collection(collection_name)
	except Exception as e:
		pass

	# Embedding function
	sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
		model_name="all-MiniLM-L6-v2"
	)

	# Creating new collection.
	return client.create_collection(
		name=collection_name,
		metadata=collection_metadata,
		configuration={
			"hsnw": {"space": "cosine"},
			"embedding_function": sentence_transformer_ef
		}
	)

def populate_similarity_collection(collection, food_items: List[Dict]):
	"""
	Populating the collection and adding it to the chromadb
	"""
	print("---- populate_similarity_collection ----")
	docs, mtds, ids = [], [], []
	used_ids = set()

	for i, food in enumerate(food_items):
	# Food Docs.
		text = f"Name: {food['food_name']}."
		text += f"Description: {food.get('food_description', '')}."
		text += f"Ingredients: {', '.join(food.get('food_ingredients', []))}."
		text += f"Cuisine: {food.get('cuisine_type', 'Unknown')}."
		text += f"Cooking Method: {food.get('cooking_method', '')}."

		# Adding food taste
		taste_profile = food.get('taste_profile', '')
		if taste_profile:
			text += f"Taste and features: {taste_profile}"

		# Adding health benefits
		health_bnfts = food.get('food_health_benefits', '')
		if health_bnfts:
			text += f"Health benefits: {health_bnfts}"

		# Adding nutritional inforation.
		if 'food_nutritional_factors' in food:
			nutrition = food['food_nutritional_factors']
			if isinstance(nutrition, dict):
				nutrition_text = ', '.join([f"{k}: {v}" for k, v in nutrition.items()])
				text += f"Nutrition: {nutrition_text}"

		# Unique id generation to avoid the duplicates.
		base_id = str(food.get('food_id', i))
		unique_id = base_id
		count = 1
		while unique_id in used_ids:
			unique_id = f"{base_id}_{count}"
			count += 1
		used_ids.add(unique_id)

		docs.append(text)
		ids.append(unique_id)
		mtds.append({
			"name": food["food_name"],
			"cuisine_type": food.get("cuisine_type", "Unknown"),
			"ingredients": ', '.join(food.get('food_ingredients', [])),
			"calories": food.get('food_calories_per_serving', 0),
			"description": food.get('food_description', ''),
			"cooking_method":food.get('cooking_method', ''),
			"health_benefits": food.get('food_health_benefits', ''),
			"taste_profile":food.get('taste_profile', '')
		})
	# Adding all to collection.
	collection.add(
		documents=docs,
		metadatas=mtds,
		ids=ids
	)
	print(f"Added {len(food_items)} food items to the collection!")

# Basic similarity search.
def perform_similarity_search(collection, query: str, n_results: int=5) -> List[Dict]:
	print("---- perform_similarity_search ----")
	try:
		results = collection.query(
			query_texts=[query],
			n_results=n_results
		)

		if not results or not results['ids'] or len(results['ids'][0]) == 0:
			return []
		
		formatted_results = []

		for i in range(len(results['ids'][0])):
			# Calculating the similarity score(1 - distance)
			sim_score = 1 - results['distances'][0][i]
			result = {
                'food_id': results['ids'][0][i],
                'food_name': results['metadatas'][0][i]['name'],
                'food_description': results['metadatas'][0][i]['description'],
                'cuisine_type': results['metadatas'][0][i]['cuisine_type'],
                'food_calories_per_serving': results['metadatas'][0][i]['calories'],
                'similarity_score': sim_score,
                'distance': results['distances'][0][i]
            }
			formatted_results.append(result)
		return formatted_results
	except Exception as e:
		print(f"Error in similarity search: {e}")
		return []
	
# Metadata filter.
def perform_filtered_similarity_search(collection, query: str, cuisine_filter: str = None,
									   max_calories: int = None, n_results: int = 5) -> List[Dict]:
	print("---- perform_filtered_similarity_search ----")
	filters = []
	if cuisine_filter:
		filters.append({'cuisine_filter': cuisine_filter})
	if max_calories:
		filters.append({'max_calories': max_calories})

	# Where clause based on the number of filters
	where_clause = filters[0] if len(filters) == 1 else {"$and": filters} if len(filters) > 1 else None

	try:
		results = collection.query(
			query_texts = [query],
			n_results = n_results,
			where = where_clause
		)
		if not results or not results['ids'] or len(results['ids'][0]) == 0:
			return []
        
		formatted_results = []
		for i in range(len(results['ids'][0])):
			similarity_score = 1 - results['distances'][0][i]
			
			result = {
				'food_id': results['ids'][0][i],
				'food_name': results['metadatas'][0][i]['name'],
				'food_description': results['metadatas'][0][i]['description'],
				'cuisine_type': results['metadatas'][0][i]['cuisine_type'],
				'food_calories_per_serving': results['metadatas'][0][i]['calories'],
				'similarity_score': similarity_score,
				'distance': results['distances'][0][i]
			}
			formatted_results.append(result)
		
		return formatted_results
	except Exception as e:
		print(f"Error in filtered search: {e}")
		return []