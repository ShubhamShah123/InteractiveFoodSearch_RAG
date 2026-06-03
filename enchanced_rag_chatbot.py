from shard_functions import *
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

import json
import os

load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

food_items = []

# LLM Model
model = ChatGoogleGenerativeAI(
	model="gemini-2.5-flash-lite",
	temperature=0.5,  # Gemini 3.0+ defaults to 1.0
	google_api_key=GEMINI_API_KEY
)


def show_enhanced_rag_help():
	"""Display help information for enhanced RAG chatbot"""
	print("\n📖 ENHANCED RAG CHATBOT HELP")
	print("This chatbot uses IBM Granite to understand your")
	print("   food preferences and provide intelligent recommendations.")
	print("\nHow to get the best recommendations:")
	print("\t• Be specific: 'healthy Italian pasta under 350 calories'")
	print("\t• Mention preferences: 'spicy comfort food for cold weather'")
	print("\t• Include context: 'light breakfast for busy morning'")
	print("\t• Ask about benefits: 'protein-rich foods for workout recovery'")
	print("\nSpecial features:")
	print("\t• 🔍 Vector similarity search finds relevant foods")
	print("\t• 🧠 AI analysis provides contextual explanations")
	print("\t• 📊 Detailed nutritional and cuisine information")
	print("\t• 🔄 Smart comparison between different preferences")
	print("\nCommands:")
	print("\t• 'compare' - AI-powered comparison of two queries")
	print("\t• 'help' - Show this help menu")
	print("\t• 'quit' - Exit the chatbot")
	print("\nTips for better results:")
	print("\t• Use natural language - talk like you would to a friend")
	print("\t• Mention dietary restrictions or preferences")
	print("\t• Include meal timing (breakfast, lunch, dinner)")
	print("\t• Specify if you want healthy, comfort, or indulgent options")

def generate_llm_comparison(query1, query2, results1, results2):
	"""Generate AI-powered comparison between two queries"""
	print("[+] Generate LLM Comparision")
	try:
		context1 = prepare_context_for_llm(query1, results1[:3])
		context2 = prepare_context_for_llm(query2, results2[:3])
		
		comparison_prompt = f'''You are analyzing and comparing two different food preference queries. Please provide a thoughtful comparison.

		Query 1: "{query1}"
		Top Results for Query 1:
		{context1}

		Query 2: "{query2}"
		Top Results for Query 2:
		{context2}

		Please provide a short comparison that:
		1. Highlights the key differences between these two food preferences
		2. Notes any similarities or overlaps
		3. Explains which query might be better for different situations
		4. Recommends the best option from each query
		5. Keeps the analysis concise but insightful

		Comparison:'''

		generated_response = model.generate(prompt=comparison_prompt, params=None)
		
		if generated_response and "results" in generated_response:
			return generated_response["results"][0]["generated_text"].strip()
		else:
			return generate_simple_comparison(query1, query2, results1, results2)
			
	except Exception as e:
		return generate_simple_comparison(query1, query2, results1, results2)

def generate_simple_comparison(query1: str, query2: str, results1: List[Dict], results2: List[Dict]) -> str:
	"""Simple comparison fallback"""
	print("[+] Generate Simple Comparision")
	if not results1 and not results2:
		return "No results found for either query."
	if not results1:
		return f"Found results for '{query2}' but none for '{query1}'."
	if not results2:
		return f"Found results for '{query1}' but none for '{query2}'."

	return f"For '{query1}', I recommend {results1[0]['food_name']}. For '{query2}', {results2[0]['food_name']} would be perfect."

def handle_enhanced_comparision_mode(collection):
	print("\n🔄 ENHANCED COMPARISON MODE")
	print("   Powered by AI Analysis")
	print("-" * 35)

	query1 = input("Enter first food query: ").strip()
	query2 = input("Enter second food query: ").strip()

	if not query1 or not query2:
		print("❌ Please enter both queries for comparison")
		return

	print(f"\n🔍 Analyzing '{query1}' vs '{query2}' with AI...")

	# Get results for both queries
	results1 = perform_similarity_search(collection, query1, 3)
	results2 = perform_similarity_search(collection, query2, 3)

	# Generate AI-powered comparison
	comparison_response = generate_llm_comparison(query1, query2, results1, results2)

	print(f"\n🤖 AI Analysis: {comparison_response}")

	# Show side-by-side results
	print(f"\n📊 DETAILED COMPARISON")
	print("=" * 60)
	print(f"{'Query 1: ' + query1[:20] + '...' if len(query1) > 20 else 'Query 1: ' + query1:<30} | {'Query 2: ' + query2[:20] + '...' if len(query2) > 20 else 'Query 2: ' + query2}")
	print("-" * 60)

	max_results = max(len(results1), len(results2))
	for i in range(min(max_results, 3)):
		left = f"{results1[i]['food_name']} ({results1[i]['similarity_score']*100:.0f}%)" if i < len(results1) else "---"
		right = f"{results2[i]['food_name']} ({results2[i]['similarity_score']*100:.0f}%)" if i < len(results2) else "---"
		print(f"{left[:30]:<30} | {right[:30]}")

def handle_enhanced_rag_query(collection, query: str, conversation_history: List[str]):
	print("[+] Handle enchanced RAG query.")
	search_results = perform_similarity_search(collection, query, 3)
	if not search_results:
		print("\t> BOT: Couldnot find any items matching the description. Try different words!")
		return

	print(f"[+] Found {len(search_results)} relevant matches.")
	print("[+] Generating the AI-powered response.")
	ai_response = generate_llm_rag_response(query, search_results)
	print(f"> BOT: {ai_response}")
	print("[+] Search Results:")
	for i, res in enumerate(search_results[:3], 1):
		print(f"{i}. {res['food_name']}")
		print(f"\t{res['cuisine_type']} | {res['food_calories_per_serving']}  cal | {res['similarity_score']*100:.1f}%")
		if i < 3:
			print()

def enhanced_rag_food_chatbot(collection):
	print("\n" + "="*70)
	print("[+] ENHANCED RAG FOOD RECOMMENDATION CHATBOT")
	print("="*70)
	print("\nExample queries:")
	print("\t• 'I want something spicy and healthy for dinner'")
	print("\t• 'What Italian dishes do you recommend under 400 calories?'")
	print("\t• 'I'm craving comfort food for a cold evening'")
	print("\t• 'Suggest some protein-rich breakfast options'")
	print("\nCommands:")
	print("\t• 'help' - Show detailed help menu")
	print("\t• 'compare' - Compare recommendations for two different queries")
	print("\t• 'quit' - Exit the chatbot")
	print("-" * 70)

	conversation_history = []
	while True:
		try:
			user_input = input("You: ").strip()
			if not user_input:
				print("> BOT: Please describe the food!")
				continue
			if user_input.lower() in ['quit', 'exit', 'q']:
				print("\n\n> BOT: GoodBye!")
				break
			elif user_input.lower() in ['help', 'h']:
				show_enhanced_rag_help()

			elif user_input.lower() in ['compare', 'c']:
				handle_enhanced_comparision_mode(collection)
			
			else:
				handle_enhanced_rag_query(collection, user_input, conversation_history)
				conversation_history.append(user_input)

				if len(conversation_history) > 5:
					conversation_history = conversation_history[-3:]

		except KeyboardInterrupt as e:
			print("\n\n> BOT: GoodBye!")
			break
		except Exception as e:
			print(f"> BOT: Sorry, Error: {e}")
		# end try

def generate_llm_rag_response(query: str, search_results: List[Dict]) -> str:
	print("[+] Generate LLM RAG Response")
	try:
		context = prepare_context_for_llm(query, search_results)
		print("[x] Context Done!")
		prompt = f'''You are a helpful food recommendation assistant. A user is asking for 	food recommendations, and I've retrieved relevant options from a food database.

		User Query: "{query}"

		Retrieved Food Information:
		{context}

		Please provide a helpful, short response that:
		1. Acknowledges the user's request
		2. Recommends 2-3 specific food items from the retrieved options
		3. Explains why these recommendations match their request
		4. Includes relevant details like cuisine type, calories, or health benefits
		5. Uses a friendly, conversational tone
		6. Keeps the response concise but informative

		Response:'''

		# Generate response
		gen_response = model.invoke(prompt, config=None)
		print("[x] Gen response")
		if gen_response and gen_response.content:
			resp_text = gen_response.text
			resp_text = resp_text.strip()

			if len(resp_text) < 50: return generate_fallback_response(query, search_results)
			return resp_text
		else:
			return generate_fallback_response(query, search_results)

	except Exception as e:
		print(f"[-] LLM Error: {e}")
		return generate_fallback_response(query, search_results)

def generate_fallback_response(query: str, search_results: List[Dict]) -> str:
	print("[+] Faillback respoinse")
	if not search_results:
		return "I could not find any food items matching the request. Try describing with different words!"
	top_results = search_results[0]
	resp_parts = []
	resp_parts.append(f"Based on the request of '{query}', I'd recommend {top_results['food_name']}.")
	resp_parts.append(f"It's a {top_results['cuisine_type']} dish with {top_results['food_calories_per_serving']} calories per serving.")

	if len(search_results) > 1:
		second_choice = search_results[1]
		resp_parts.append(f"Another great option would be {second_choice['food_name']}")
	return " ".join(resp_parts)

def prepare_context_for_llm(query: str, search_results: List[Dict]) -> str:
	print("[+] Prepare context for LLM")
	if not search_results:
		return "No relevant food items found in DB."

	context_parts = []
	context_parts.append("Based on the query, here are the most relevant food options:")
	context_parts.append("")

	for i, result in enumerate(search_results[:3], 1):
		food_context = []
		food_context.append(f"Option {i}: {result['food_name']}")
		food_context.append(f"\t- Description: {result['food_description']}")
		food_context.append(f"\t- Cuisine: {result['cuisine_type']}")
		food_context.append(f"\t- Calories: {result['food_calories_per_serving']} cal per serving")

		if result.get('food_ingredients'):
			ingredients = result['food_ingredients']
			if isinstance(ingredients, list):
				food_context.append(f"\t- Key Ingredients: {', '.join(ingredients[:5])}")
			else:
				food_context.append(f"\t- Key Ingredients: {ingredients}")

		if result.get('food_health_benefits'):
			food_context.append(f"\t- Health Benefits: {result['food_health_benefits']}")

		if result.get('cooking_method'):
			food_context.append(f"\t- Cooking Method: {result['cooking_method']}")

		if result.get('taste_profile'):
			food_context.append(f"\t- Taste Profile: {result['taste_profile']}")

		food_context.append(f"\t- Similarity Score: {result['similarity_score']*100:.1f}%")
		food_context.append("")

		context_parts.extend(food_context)
	return "\n".join(context_parts)

def main():
	try:
		print("#### Enchanced RAG-Powered Foor Recommendation Chatbot ####")
		print("="*25)

		global food_items
		food_items = load_food_data('./FoodDataSet.json')
		print(f"Loaded {len(food_items)} food items!")

		# Creating collection.
		collection = create_similarity_search_collection(
			"enhanced_rag_food_chatbot",
			{'description': 'Enhanced RAG chatbot using Gemini API.'}
		)

		populate_similarity_collection(collection, food_items)
		print("Vector Database ready!")

		# Testing LLM Connection.
		print("[+] Testing LLM Connection...")
		test_resp = model.invoke("Hello")
		if test_resp and test_resp.content:
			print("[Y] LLM Connection Successful! ")
		else:
			print("[N] LLM Connection failed!")

		enhanced_rag_food_chatbot(collection)
	except Exception as e:
		print(f"ERROR: {e}")

if __name__ == "__main__":
	main()