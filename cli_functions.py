from shard_functions import perform_similarity_search

def suggest_related_searches(results):
    """Suggest related searches based on current results"""
    if not results:
        return
    
    # Extract cuisine types from results
    cuisines = list(set([r['cuisine_type'] for r in results]))
    
    print("\n💡 Related searches you might like:")
    for cuisine in cuisines[:3]:  # Limit to 3 suggestions
        print(f"\t\t• Try '{cuisine} dishes' for more {cuisine} options")
    
    # Suggest calorie-based searches
    avg_calories = sum([r['food_calories_per_serving'] for r in results]) / len(results)
    if avg_calories > 350:
        print("\t\t• Try 'low calorie' for lighter options")
    else:
        print("\t\t• Try 'hearty meal' for more substantial dishes")

def handle_food_search(collection, query):
    """Handle food similarity search with enhanced display"""
    print(f"\n🔍 Searching for '{query}'...")
    print("   Please wait...")
    
    # Perform similarity search
    results = perform_similarity_search(collection, query, 5)
    
    if not results:
        print("❌ No matching foods found.")
        print("💡 Try different keywords like:")
        print("\t\t• Cuisine types: 'Italian', 'American'")
        print("\t\t• Ingredients: 'chocolate', 'flour', 'cheese'")
        print("\t\t• Descriptors: 'sweet', 'baked', 'dessert'")
        return
    
    # Display results with rich formatting
    print(f"\n✅ Found {len(results)} recommendations:")
    print("=" * 60)
    
    for i, result in enumerate(results, 1):
        # Calculate percentage score
        percentage_score = result['similarity_score'] * 100
        
        print(f"\n{i}. 🍽️  {result['food_name']}")
        print(f"\t\t📊 Match Score: {percentage_score:.1f}%")
        print(f"\t\t🏷️  Cuisine: {result['cuisine_type']}")
        print(f"\t\t🔥 Calories: {result['food_calories_per_serving']} per serving")
        print(f"\t\t📝 Description: {result['food_description']}")
        
        # Add visual separator
        if i < len(results):
            print("   " + "-" * 50)
    
    print("=" * 60)
    
    # Provide suggestions for further exploration
    suggest_related_searches(results)

def show_help_menu():
    """Display help information for users"""
    print("\n📖 HELP MENU")
    print("-" * 30)
    print("Search Examples:")
    print("\t• 'chocolate dessert' - Find chocolate desserts")
    print("\t• 'Italian food' - Find Italian cuisine")
    print("\t• 'sweet treats' - Find sweet desserts")
    print("\t• 'baked goods' - Find baked items")
    print("\t• 'low calorie' - Find lower-calorie options")
    print("\nCommands:")
    print("\t• 'help' - Show this help menu")
    print("\t• 'quit' - Exit the system")

def interactive_chat_bot(collection):
    """Interactive CLI Chatbot for food recommendation"""
    print("\n"+"="*50)
    print("FOOD SEARCH CHATBOT.")
    print("="*50)
    print("Commands:")
    print("\t• Type any food name or description to search")
    print("\t• 'help' - Show available commands")
    print("\t• 'quit' or 'exit' - Exit the system")
    print("\t• Ctrl+C - Emergency exit")
    print("-"*50)

    while True:
        try:
            user_input = input("\nSearch for food: ").strip()
            if not user_input:
                print("\tPlease enter a search term or 'help' for commands.")
                continue
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n\tGoodBye!")
                break
            elif user_input.lower() in ['help', 'h']:
                show_help_menu()
            else:
                handle_food_search(collection, user_input)
        except KeyboardInterrupt as e:
            print("\n\nSystem Interruption: ", e)
            break
        except Exception as e:
            print("\n\nError: ", e)

        # end try
