from shard_functions import *
from advanced_search_functions import *

def main():
    try:
        print("ADVANCED FOOD SEARCH SYSTEM")
        print("-"*50)
        print("Loading food db with advanced filtering capabilities...")

        food_items = load_food_data('./FoodDataSet.json')
        print(f"Loaded {len(food_items)} food items successfully!")

        # advanced search collection.

        collection = create_similarity_search_collection(
            "advanced_food_search",
            {'description':'A collection for advanced search demos.'}
        )

        populate_similarity_collection(collection, food_items)

        # start the advanced search
        interactive_advanced_search(collection)
    except Exception as e:
        print(f"Error initializing advanced search system: {e}")

if __name__ == "__main__":
    main()