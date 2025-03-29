import json
import random


def load_data(json_file):
    """Load and parse the science gateway JSON data."""
    with open(json_file, "r", encoding="utf-8") as file:
        return json.load(file)


def search_gateway(query, data):
    """Simple keyword-based search for relevant science gateway tools."""
    query = query.lower()
    results = [
        item for item in data
        if query in item["name"].lower() or query in item["abstract"].lower() or any(
            query in tag.lower() for tag in item["tags"])
    ]
    return results if results else None


def chatbot():
    """Basic chatbot loop for interactive queries."""
    print("\n🤖 Science Gateway Chatbot: Ask me about research tools! Type 'exit' to quit.\n")
    data = load_data("science_gateways_extended.json")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye! 👋")
            break

        results = search_gateway(user_input, data)
        if results:
            response = random.choice(results)  # Pick a random relevant result
            print(f"\n🔹 {response['name']}")
            print(f"📄 {response['abstract']}")
            print(f"🔗 More info: {response['site']}")
            print(f"🏷 Tags: {', '.join(response['tags']) if response['tags'] else 'None'}\n")
        else:
            print("❌ No matching resources found. Try another query!\n")


if __name__ == "__main__":
    chatbot()
