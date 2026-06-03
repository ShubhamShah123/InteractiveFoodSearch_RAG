from shard_functions import *
from cli_functions import *
# Global list to store items
food_items = []

def main():
    try:
        print("####### INTERACTIVE FOOD RECOMMNEDATION SYSTEM #######")
        print("-"*50)
        print("Loading food database...")

        global food_items
        food_items = load_food_data('./FoodDataSet.json')
        print(f"Loaded {len(food_items)} food items successfully!")

        # Craeting and populating the collection.
        collection = create_similarity_search_collection(
            "interactive_food_search",
            {'description': 'A collection for interactive food search'}
        )

        populate_similarity_collection(collection, food_items)
        
        # Starting the chatbot.
        interactive_chat_bot(collection)

    except Exception as e:
        print(f"Error starting system: {e}")
    
if __name__ == "__main__":
    main()