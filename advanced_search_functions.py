from shard_functions import *
import sys

def display_search_results(results, title, showDetails=True):
	print(f"#### {title} ####")
	if not results:
		print("\t[-] No results found.")
		return
	for i, result in enumerate(results, 1):
		score = result['similarity_score'] * 100
		if showDetails:
			print(f"\n{i}. {result['food_name']}")
			print(f"> Similarity Score: {score:.1f}%")
			print(f"> Cuisine: {result['cuisine_type']}")
			print(f"> Calories: {result['food_calories_per_serving']}")
			print(f"> Description: {result['food_description']}")
		else:
			print(f"\n{i}. {result['food_name']}")
	print("#"*10)

def perform_basic_search(collection):
	print("[+] Performing basic similarity search ...")
	query = input("Enter search query: ").strip()
	if not query:
		print("\t[-] Please enter a search term.")
		return
	print(f"\t[X] Searching for '{query}'")
	results = perform_similarity_search(collection, query, 5)
	display_search_results(results, "Basic Similarity Results")

def perform_cuisine_filtered_search(collection):
	print("[+] Performing cuisine filtered search ...")

	# Cuisine List
	cuisines = ["Italian", "Thai", "Mexican", "Indian", "Japanese", "French", 
				"Mediterranean", "American", "Health Food", "Dessert"]
	
	print("Available Cuisines:")
	for i, val in enumerate(cuisines, 1):
		print(f"\t{i}. {val}")

	query = input("\nEnte the search query: ").strip()
	cuisine_choice = input("Enter the cuisine number or name: ").strip()
	if not query:
		print("[-] Enter a search term.")
		return
	
	cuisine_filter = None
	if cuisine_choice.isdigit():
		idx = int(cuisine_choice) - 1
		cuisine_filter = cuisines[idx] if idx in range(0, len(cuisines)) else cuisine_choice
		
	if not cuisine_filter:
		print("[-] Invalid cuisine selection.")
		return
	print(f"\t[X] Searching for '{query}' in {cuisine_filter} cuisine...")
	result = perform_filtered_similarity_search(
		collection, query, cuisine_filter=cuisine_filter, n_results=5
	)
	display_search_results(result, f"Cuisine-Filtered Results - {cuisine_filter}")

def perform_calorie_filtered_search(collection):
	
	print("[+] Performing Calorie-Filteted Search")
	# Cuisine List
	
	query = input("\nEnte the search query: ").strip()
	max_cal_input = input("Enter maximum calorie(or Enter for no limit): ").strip()

	if not query:
		print("[-] Enter a search term.")
		return
	
	max_calories = int(max_cal_input) if max_cal_input.isdigit() else None

	print(f"\t[X] Searching for '{query}'" + f" with max {max_calories} calories..." if max_calories else "...")
	result = perform_filtered_similarity_search(
		collection, query, max_calories=max_calories, n_results=5
	)
	calorie_text = f"under {max_calories} calories" if max_calories else "any calories"
	display_search_results(result, f"Calorie-Filtered Results - {calorie_text}")

def perform_combined_filtered_search(collection):
	"""Perform search with multiple filters combined"""
	print("\n[+] Combined Filtered Search.")

	query = input("Enter search query: ").strip()
	cuisine = input("Enter cuisine type (optional): ").strip()
	max_calories_input = input("Enter maximum calories (optional): ").strip()

	if not query:
		print("❌ Please enter a search term")
		return

	cuisine_filter = cuisine if cuisine else None
	max_calories = int(max_calories_input) if max_calories_input.isdigit() else None

	# Build description of applied filters
	filter_description = []
	if cuisine_filter:
		filter_description.append(f"cuisine: {cuisine_filter}")
	if max_calories:
		filter_description.append(f"max calories: {max_calories}")

	filter_text = ", ".join(filter_description) if filter_description else "no filters"

	print(f"\n🔍 Searching for '{query}' with {filter_text}...")

	results = perform_filtered_similarity_search(
		collection, query, 
		cuisine_filter=cuisine_filter, 
		max_calories=max_calories, 
		n_results=5
	)

	display_search_results(results, f"Combined Filtered Results ({filter_text})")

def demo_mode(collection):
	print("\n[+] Demonstration Mode.")
	demonstrations = [
		{
			"title": "Italian Cuisine Search",
			"query": "creamy pasta",
			"cuisine_filter": "Italian",
			"max_calories": None
		},
		{
			"title": "Low-Calorie Healthy Options",
			"query": "healthy meal",
			"cuisine_filter": None,
			"max_calories": 300
		},
		{
			"title": "Asian Light Dishes",
			"query": "light fresh meal",
			"cuisine_filter": "Japanese",
			"max_calories": 250
		}
	]
	
	for i, demo in enumerate(demonstrations, 1):
		print(f"\n{i}. {demo['title']}")
		print(f"   Query: '{demo['query']}'")
		
		filters = []
		if demo['cuisine_filter']:
			filters.append(f"Cuisine: {demo['cuisine_filter']}")
		if demo['max_calories']:
			filters.append(f"Max Calories: {demo['max_calories']}")
		
		if filters:
			print(f"   Filters: {', '.join(filters)}")
		
		results = perform_filtered_similarity_search(
			collection,
			demo['query'],
			cuisine_filter=demo['cuisine_filter'],
			max_calories=demo['max_calories'],
			n_results=3
		)
		
		display_search_results(results, demo['title'], showDetails=False)
		
		input("\n⏸️  Press Enter to continue to next demonstration...")

def advanced_help(collection):
	"""Display help information for advanced search"""
	print("\n[+] ADVANCED SEARCH HELP")
	print("Search Types:")
	print("\t1. Basic Search - Standard similarity search")
	print("\t2. Cuisine Filter - Search within specific cuisine types")
	print("\t3. Calorie Filter - Search for foods under calorie limits")
	print("\t4. Combined Filters - Use multiple filters together")
	print("\t5. Demonstrations - See predefined search examples")
	print("\nTips:")
	print("\t• Use descriptive terms: 'creamy', 'spicy', 'light'")
	print("\t• Combine ingredients: 'chicken vegetables'")
	print("\t• Try cuisine names: 'Italian', 'Thai', 'Mexican'")
	print("\t• Filter by calories for dietary goals")

def interactive_advanced_search(collection):
	menu_options = {
		1: {
			'name': 'Basic Similarity search',
			'action': perform_basic_search
		},
		2: {
			'name': 'Cuisine-filtered search',
			'action': perform_cuisine_filtered_search
		},
		3: {
			'name': 'Calorie-filtered search',
			'action': perform_calorie_filtered_search
		},
		4: {
			'name': 'Combined filters search',
			'action': perform_combined_filtered_search
		},
		5: {
			'name': 'Demo mode',
			'action': demo_mode
		},
		6: {
			'name': 'Help',
			'action': advanced_help
		},
		7: {
			'name': 'Exit',
			'action':  lambda _: sys.exit(0)
		},
	}
	print("="*50)
	print("ADVANCED SEARCH WITH FILTERS")
	print("="*50)
	print("Search Options:")
	for k, v in menu_options.items():
		print(f"\t{k}: {v['name']}")

	while True:
		try:
			choice = int(input("Select Option(1-7):"))
			resp = menu_options.get(choice)
			resp['action'](collection)


		except KeyboardInterrupt as e:
			print("\nSYSTEM INTERRUPTED.")
			break
		except Exception as e:
			print(f"ERROR: {e}")