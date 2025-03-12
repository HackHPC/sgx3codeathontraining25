import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import threading
import json

class ScienceGatewayGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Science Gateway Assistant")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        self.root.iconbitmap('snowflake_2\images\craiyon_181200_snowflake_with_face_cartoon_blue_and_happy.png') if hasattr(root, 'iconbitmap') else None

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

        send_button = ttk.Button(
            input_frame,
            text="Send",
            command=self.send_message
        )
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
        self.chat_display.tag_configure("user_msg", foreground="black", font=("Arial", 10))
        self.chat_display.tag_configure("bot", foreground="green", font=("Arial", 10, "bold"))
        self.chat_display.tag_configure("bot_msg", foreground="black", font=("Arial", 10))
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
            self.root.after(0, lambda: self.update_chat_display("System", "Ready"))
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            self.root.after(0, lambda: self.update_chat_display("System", error_msg))
            self.root.after(0, lambda: self.update_chat_display("System", "Ready"))
        finally:
            self.root.after(0, lambda: self.user_input.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.user_input.focus_set())

    def load_json_data(self):
        try:
            filepath = r"C:\Users\admin\Downloads\SGX3Project-CM\snowflake\science_gateways_extended.json"

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.gateway_data['definitions'] = ["Science gateways are web-based interfaces that provide researchers with access to advanced resources, tools, and data for specific scientific disciplines."]

            for entry in data:
                all_text = " ".join(str(entry.get(field, '')).lower() for field in ['name', 'category', 'abstract', 'site', 'published_on', 'site_url', 'cite'])
                tags = " ".join(str(tag).lower() for tag in entry.get('tags', []))
                all_text += " " + tags
                entry['all_text'] = all_text

            self.gateway_data['gateways'] = data
            self.data_loaded = True
            self.root.after(0, lambda: self.status_label.config(text="Status: Data loaded from JSON"))

        except FileNotFoundError:
            error_message = "JSON file not found. Ensure the path is correct."
            self.root.after(0, lambda: messagebox.showerror("File Error", error_message))
            self.root.after(0, lambda: self.status_label.config(text="Status: JSON load failed"))
        except json.JSONDecodeError:
            error_message = "Error decoding JSON. Ensure the file is valid JSON."
            self.root.after(0, lambda: messagebox.showerror("JSON Error", error_message))
            self.root.after(0, lambda: self.status_label.config(text="Status: JSON load failed"))
        except Exception as e:
            error_message = f"An unexpected error occurred during JSON loading: {str(e)}"
            self.root.after(0, lambda: messagebox.showerror("JSON Error", error_message))
            self.root.after(0, lambda: self.status_label.config(text="Status: JSON load failed"))

    def search_gateways(self, query):
        """Search for science gateways related to the user's query, focusing on category and tags."""
        if not self.data_loaded:
            return []

        results = []
        query_lower = query.lower().split()

        # Iterate through the gateway data
        for entry in self.gateway_data['gateways']:
            category = entry.get('category', '').lower()  # Get category
            tags = entry.get('tags', [])  # Get tags (list of tags)
            description = entry.get('abstract', '').lower()  # Get description

            # Start a score for each entry
            score = 0

            # Check if the query matches in the category field
            if any(word in category for word in query_lower):
                score += 3  # High priority match in category

            # Check if the query matches any of the tags
            if any(word in tags for word in query_lower):
                score += 2  # Moderate priority match in tags

            # Check if the query matches any part of the description (abstract)
            if any(word in description for word in query_lower):
                score += 1  # Lower priority match in description

            # If there's a positive score, the entry is relevant to the query
            if score > 0:
                results.append((score, entry))

        # Sort the results by score (highest first)
        results.sort(key=lambda x: x[0], reverse=True)

        # Return only the gateway data entries, excluding the score
        return [entry for score, entry in results]

    def query_data(self, prompt):
        try:
            prompt_lower = prompt.lower()

            if "what is a science gateway" in prompt_lower or "define science gateway" in prompt_lower:
                if self.gateway_data['definitions']:
                    return f"A science gateway can be defined as: \n{self.gateway_data['definitions'][0]}"
                else:
                    return "I couldn't find a specific definition in the data."

            gateway_results = self.search_gateways(prompt)

            if gateway_results:
                response = "Here are some relevant science gateways:\n"
                for gateway in gateway_results[:3]:  # Limit to top 3 results
                    response += f"- {gateway.get('name', 'N/A')}: {gateway.get('abstract', 'N/A')}\n"
                return response

            return "I'm sorry, I couldn't find any specific information related to your query."

        except Exception as e:
            return f"An error occurred while processing your request: {str(e)}"

if __name__ == "__main__":
    root = tk.Tk()
    app = ScienceGatewayGUI(root)
    root.mainloop()
