import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import threading
import json
import requests
from bs4 import BeautifulSoup
import spacy

nlp = spacy.load("en_core_web_sm")  
 
class ScienceGatewayGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Science Gateway Assistant")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        self.gateway_data = {
            'definitions': [],
            'gateways': []
        }
        self.data_loaded = False
        self.setup_ui()
        threading.Thread(target=self.load_json_data, daemon=True).start()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        chat_frame = ttk.Frame(notebook)
        notebook.add(chat_frame, text="Chat")
        self.setup_chat_interface(chat_frame)

        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label = ttk.Label(
            status_frame,
            text=f"Status: {'Ready' if self.data_loaded else 'Data not loaded'}"
        )
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
# Load a larger pre-trained NLP model (e.g., en_core_web_lg)
nlp = spacy.load("en_core_web_lg")

class ScienceGatewayGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Science Gateway Assistant")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        self.gateway_data = {
            'definitions': [],
            'gateways': []
        }
        self.data_loaded = False
        self.setup_ui()
        threading.Thread(target=self.load_json_data, daemon=True).start()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        chat_frame = ttk.Frame(notebook)
        notebook.add(chat_frame, text="Chat")
        self.setup_chat_interface(chat_frame)

        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        self.status_label = ttk.Label(
            status_frame,
            text=f"Status: {'Ready' if self.data_loaded else 'Data not loaded'}"
        )
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)

    def setup_chat_interface(self, parent):
        chat_frame = ttk.Frame(parent)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=("Arial", 10)
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_display.config(state=tk.DISABLED)

        self.update_chat_display("System", "Welcome to the Science Gateways Assistant!\n")
        self.update_chat_display(
            "System",
            "Try questions like:\n- Tell me about science gateways\n- What gateways are available for computational research?\n"
        )

        input_frame = ttk.Frame(parent)
        input_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)

        self.user_input = ttk.Entry(input_frame, font=("Arial", 10))
        self.user_input.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=(0, 5))
        self.user_input.bind("<Return>", self.send_message)

        send_button = ttk.Button(input_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.RIGHT)
        self.user_input.focus_set()

    def update_chat_display(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        if sender == "User":
            self.chat_display.insert(tk.END, f"\n{sender}: ", "user")
            self.chat_display.insert(tk.END, f"{message}\n", "user_msg")
        elif sender == "Bot":
            self.chat_display.insert(tk.END, f"\n{sender}: ", "bot")
            self.chat_display.insert(tk.END, f"{message}\n", "bot_msg")
        else:
            self.chat_display.insert(tk.END, f"{message}\n", "system")

        self.chat_display.tag_configure("user", foreground="blue", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("user_msg", foreground="black")
        self.chat_display.tag_configure("bot", foreground="green", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("bot_msg", foreground="black")
        self.chat_display.tag_configure("system", foreground="gray", font=("Arial", 9, "italic"))
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def send_message(self, event=None):
        message = self.user_input.get().strip()
        if not message:
            return

        self.update_chat_display("User", message)
        self.user_input.delete(0, tk.END)
        self.user_input.config(state=tk.DISABLED)
        self.update_chat_display("System", "Processing...")

        if not self.data_loaded:
            self.update_chat_display("System", "Warning: Gateway data not loaded. Responses may be limited.")

        threading.Thread(target=self.process_message, args=(message,), daemon=True).start()

    def process_message(self, message):
        try:
            response = self.query_data(message)
            self.root.after(0, lambda: self.update_chat_display("Bot", response))
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            self.root.after(0, lambda: self.update_chat_display("System", error_msg))
        finally:
            self.root.after(0, lambda: self.user_input.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.user_input.focus_set())
            self.root.after(0, lambda: self.update_chat_display("System", "Ready"))

    def load_json_data(self):
        try:
            filepath = r"C:\Users\admin\Downloads\SGX3Project-CM\sgx3_code_coreen\science_gateways_extended.json"
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.gateway_data['definitions'] = [
                "Science gateways are web-based interfaces that provide researchers with access to advanced resources, tools, and data for specific scientific disciplines."
            ]
            self.gateway_data['gateways'] = data
            self.data_loaded = True
            self.root.after(0, lambda: self.status_label.config(text="Status: Data loaded from JSON"))

        except FileNotFoundError:
            self.handle_error("JSON file not found. Ensure the path is correct.")
        except json.JSONDecodeError:
            self.handle_error("Error decoding JSON. Ensure the file is valid JSON.")
        except Exception as e:
            self.handle_error(f"Unexpected error during JSON loading: {str(e)}")

    def handle_error(self, message):
        self.root.after(0, lambda: messagebox.showerror("Error", message))
        self.root.after(0, lambda: self.status_label.config(text="Status: JSON load failed"))

    def fetch_website_info(self, query):
        if "faculty" in query.lower():
            try:
                response = requests.get("https://www.sciencegateways.org/")
                soup = BeautifulSoup(response.content, 'html.parser')
                faculty_info = soup.find_all('p', string=lambda text: text and 'faculty' in text.lower())
                return "\n".join(para.get_text() for para in faculty_info) if faculty_info else "No faculty info found."
            except requests.exceptions.RequestException as e:
                return f"Error accessing website: {e}"
        return None

    def query_data(self, prompt):
        website_response = self.fetch_website_info(prompt)
        if website_response:
            return website_response

        try:
            prompt_lower = prompt.lower()
            if any(q in prompt_lower for q in ["what is a science gateway", "define science gateway"]):
                return self.handle_definition_query()

            results = self.search_gateways(prompt)
            return self.format_gateway_results(results)

        except Exception as e:
            return f"Error processing request: {str(e)}"

    def handle_definition_query(self):
        if self.gateway_data['definitions']:
            return f"A science gateway can be defined as:\n{self.gateway_data['definitions'][0]}"
        return "No definition available in the data."

    def search_gateways(self, query):
        """Search for science gateways related to the user's query using semantic similarity."""
        if not self.data_loaded:
            return []

        query_doc = nlp(query)
        results = []

        for entry in self.gateway_data['gateways']:
            abstract = entry.get('abstract', '')
            if not abstract:
                continue

            abstract_doc = nlp(abstract)
            similarity_score = query_doc.similarity(abstract_doc)

            results.append((similarity_score, entry))

        # Sort by similarity score (highest first)
        results.sort(key=lambda x: x[0], reverse=True)

        # Return only the gateway data entries, excluding the score
        return [entry for score, entry in results]

    def format_gateway_results(self, results):
        if not results:
            return "No matching gateways found."
            
        response = "Top matching science gateways:\n"
        for entry in results[:3]:
            response += f"\n- {entry.get('name', 'N/A')}:\n  {entry.get('abstract', 'No description available')}\n"
        return response

if __name__ == "__main__":
    root = tk.Tk()
    app = ScienceGatewayGUI(root)
    root.mainloop()