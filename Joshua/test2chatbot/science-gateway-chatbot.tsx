<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Science Gateway Research Assistant</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }
        #chatContainer {
            border: 1px solid #ddd;
            height: 500px;
            display: flex;
            flex-direction: column;
            background-color: white;
        }
        #chatMessages {
            flex-grow: 1;
            overflow-y: auto;
            padding: 10px;
        }
        .message {
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
        }
        .bot-message {
            background-color: #e6f3ff;
            align-self: flex-start;
        }
        .user-message {
            background-color: #e6ffe6;
            align-self: flex-end;
            text-align: right;
        }
        #inputContainer {
            display: flex;
            padding: 10px;
            background-color: #f9f9f9;
        }
        #userInput {
            flex-grow: 1;
            padding: 10px;
            margin-right: 10px;
        }
        #sendButton {
            padding: 10px 20px;
        }
    </style>
</head>
<body>
    <div id="chatContainer">
        <div id="chatMessages"></div>
        <div id="inputContainer">
            <input type="text" id="userInput" placeholder="Ask about science gateways...">
            <button id="sendButton">Send</button>
        </div>
    </div>

    <script>
        // Science Gateway Data
        const scienceGateways = [
            {
                name: "Custos Admin Gateway",
                description: "Provides security services for science gateways",
                category: "Security",
                tags: ["ACCESS-CI", "Identity Management"]
            },
            {
                name: "EDGE Bioinformatics Gateway",
                description: "Process Next Generation Sequencing data for biologists",
                category: "Bioinformatics",
                tags: ["Genomics", "Research"]
            },
            {
                name: "CyberWater",
                description: "Tackle scientific questions about water resources",
                category: "Environmental Science",
                tags: ["Water", "Climate"]
            },
            {
                name: "Neuroscience Gateway",
                description: "Computational tools for neuroscience research",
                category: "Neuroscience",
                tags: ["Brain Research", "Computational Biology"]
            }
        ];

        // DOM Elements
        const chatMessages = document.getElementById('chatMessages');
        const userInput = document.getElementById('userInput');
        const sendButton = document.getElementById('sendButton');

        // Add Message to Chat
        function addMessage(message, type = 'bot') {
            const messageElement = document.createElement('div');
            messageElement.classList.add('message', `${type}-message`);
            messageElement.textContent = message;
            chatMessages.appendChild(messageElement);
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        // Process User Query
        function processQuery(query) {
            const lowercaseQuery = query.toLowerCase();

            // Intents and Matching
            const intents = [
                {
                    keywords: ['list', 'show', 'all', 'gateways'],
                    handler: () => {
                        return scienceGateways.map(gw => 
                            `${gw.name}: ${gw.description}`
                        ).join('\n');
                    }
                },
                {
                    keywords: ['search', 'find'],
                    handler: () => {
                        const matches = scienceGateways.filter(gw => 
                            gw.name.toLowerCase().includes(lowercaseQuery) ||
                            gw.description.toLowerCase().includes(lowercaseQuery) ||
                            gw.tags.some(tag => tag.toLowerCase().includes(lowercaseQuery))
                        );

                        return matches.length > 0
                            ? matches.map(gw => 
                                `Gateway: ${gw.name}\nDescription: ${gw.description}\nCategory: ${gw.category}`
                            ).join('\n\n')
                            : "No matching gateways found.";
                    }
                },
                {
                    keywords: ['help', 'what can you do'],
                    handler: () => {
                        return "I can help you with:\n" +
                               "- List all science gateways\n" +
                               "- Search for specific gateways\n" +
                               "- Find gateways by category or tags";
                    }
                }
            ];

            // Find matching intent
            const matchedIntent = intents.find(intent => 
                intent.keywords.some(keyword => 
                    lowercaseQuery.includes(keyword)
                )
            );

            // Return response
            return matchedIntent 
                ? matchedIntent.handler() 
                : "I'm not sure how to help with that. Try 'list gateways' or 'search bioinformatics'";
        }

        // Send Message Handler
        function sendMessage() {
            const message = userInput.value.trim();
            
            if (message) {
                // Add user message
                addMessage(message, 'user');
                
                // Process and add bot response
                const response = processQuery(message);
                addMessage(response, 'bot');
                
                // Clear input
                userInput.value = '';
            }
        }

        // Event Listeners
        sendButton.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Initial Welcome Message
        addMessage("Welcome to the Science Gateway Research Assistant! Type 'help' to learn what I can do.");
    </script>
</body>
</html>
