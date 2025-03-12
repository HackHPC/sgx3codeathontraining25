import json
import ollama

# Load the Science Gateways JSON data
def load_gateway_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON from {file_path}.")
        return []

# Format gateway data into a searchable string for the LLM
def format_gateway_data(gateways):
    formatted_text = ""
    for gateway in gateways:
        formatted_text += (
            f"Name: {gateway['name']}\n"
            f"Category: {gateway['category']}\n"
            f"Site: {gateway['site']}\n"
            f"Abstract: {gateway['abstract']}\n"
            f"Site URL: {gateway['site_url']}\n"
            f"Tags: {', '.join(gateway['tags'])}\n"
            f"---\n"
        )
    return formatted_text

# Query Ollama LLM with user input and gateway data
def query_ollama(prompt, gateway_data):
    full_prompt = (
        "You are a helpful assistant for faculty and researchers looking for resources on the Science Gateways website. "
        "Below is a list of Science Gateway resources. Use this information to answer the user's question accurately and concisely. "
        "If the answer isn't clear from the data, provide a general response based on your knowledge and suggest consulting the Science Gateways website for more details.\n\n"
        "Resources:\n" + gateway_data + "\n\n"
        "User Question: " + prompt + "\n\n"
        "Answer:"
    )
    
    response = ollama.generate(model="llama3", prompt=full_prompt)
    return response['response'].strip()

# Main chatbot loop
def chatbot():
    print("Welcome to the Science Gateways Chatbot!")
    print("Ask me anything about the resources listed on the Science Gateways website.")
    print("Type 'exit' to quit.\n")
    
    # Load and format the gateway data once
    gateways = load_gateway_data("science_gateways.json")
    if not gateways:
        print("Failed to load gateway data. Exiting.")
        return
    
    gateway_data = format_gateway_data(gateways)
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        if not user_input:
            print("Please ask a question!")
            continue
        
        # Get response from Ollama
        response = query_ollama(user_input, gateway_data)
        print(f"Chatbot: {response}\n")

# Run the chatbot
if __name__ == "__main__":
    chatbot()
