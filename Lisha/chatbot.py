import json
import os

# Print the current working directory to debug
print("Current working directory:", os.getcwd())

# Load the JSON file with UTF-8 encoding
try:
    with open('science_gateways_extended.json', 'r', encoding='utf-8') as file:
        gateways = json.load(file)  # Store the JSON data in a variable
except FileNotFoundError:
    print("Error: 'science_gateways_extended.json' not found. Please ensure it's in the same directory.")
    exit()
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON format in 'science_gateways_extended.json'. Details: {e}")
    exit()
except UnicodeDecodeError as e:
    print(f"Error: Unable to decode the file with UTF-8. Details: {e}")
    exit()


# Function to list all gateways
def list_gateways():
    print("\nHere are all the science gateways:")
    for gateway in gateways:
        print(f"- {gateway['name']}")
    print()


# Function to describe a specific gateway
def describe_gateway(gateway_name):
    for gateway in gateways:
        if gateway['name'].lower() == gateway_name.lower():
            print(f"\nDetails for '{gateway['name']}':")
            print(f"Description: {gateway['abstract']}")
            print(f"URL: {gateway['site_url']}")
            print(f"Category: {gateway['category']}")
            print()
            return
    print(f"\nSorry, I couldn't find '{gateway_name}' in the database.\n")


# Function to search gateways by keyword or category
def search_gateways(search_term):
    matches = []
    for gateway in gateways:
        if (search_term.lower() in gateway['name'].lower() or
                search_term.lower() in gateway['abstract'].lower() or
                search_term.lower() in gateway['category'].lower()):
            matches.append(gateway['name'])

    if matches:
        print(f"\nFound {len(matches)} gateways matching '{search_term}':")
        for match in matches:
            print(f"- {match}")
        print()
    else:
        print(f"\nNo gateways found matching '{search_term}'.\n")


# Main chatbot loop
print("Welcome to the Science Gateways Chatbot!")
print("Commands: 'list', 'describe [gateway name]', 'search [keyword]', 'quit'")

while True:
    user_input = input("What would you like to do? ").strip()
    parts = user_input.split(" ", 1)
    command = parts[0].lower()

    if command == "list":
        list_gateways()
    elif command == "describe" and len(parts) > 1:
        describe_gateway(parts[1])
    elif command == "search" and len(parts) > 1:
        search_gateways(parts[1])
    elif command == "quit":
        print("Goodbye!")
        break
    else:
        print("\nInvalid command. Please try:")
        print("- 'list' to see all gateways")
        print("- 'describe [gateway name]' to get details")
        print("- 'search [keyword]' to find gateways")
        print("- 'quit' to exit\n")