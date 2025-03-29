// Sample science gateway data
const scienceGateways = [
    {
        name: "Custos Admin Gateway",
        description: "Provides security services for science gateways",
        tags: ["ACCESS-CI", "Security"]
    },
    {
        name: "EDGE Bioinformatics Gateway",
        description: "Process Next Generation Sequencing data for biologists",
        tags: ["Bioinformatics", "Research"]
    },
    {
        name: "CyberWater",
        description: "Tackle scientific questions about water resources",
        tags: ["Environmental Science", "Water"]
    }
];

// DOM Elements
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const chatMessages = document.getElementById('chatMessages');

// Function to add a message to the chat
function addMessage(content, type = 'bot') {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${type}-message`);
    messageElement.textContent = content;
    chatMessages.appendChild(messageElement);
    
    // Scroll to bottom of messages
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Process user query
function processQuery(query) {
    const lowercaseQuery = query.toLowerCase();
    
    // Search gateways
    const matchedGateways = scienceGateways.filter(gateway => 
        gateway.name.toLowerCase().includes(lowercaseQuery) ||
        gateway.description.toLowerCase().includes(lowercaseQuery) ||
        gateway.tags.some(tag => tag.toLowerCase().includes(lowercaseQuery))
    );
    
    // Generate response
    if (matchedGateways.length > 0) {
        return matchedGateways.map(gateway => 
            `Gateway: ${gateway.name}\nDescription: ${gateway.description}\nTags: ${gateway.tags.join(', ')}`
        ).join('\n\n');
    }
    
    // Default responses
    const defaultResponses = [
        "I'm not sure about that. Can you try a different query?",
        "Could you be more specific about the science gateway you're looking for?",
        "I can help you find science gateways. Try searching by name or research area."
    ];
    
    return defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
}

// Send message handler
function sendMessage() {
    const query = userInput.value.trim();
    
    if (query) {
        // Add user message
        addMessage(query, 'user');
        
        // Process and add bot response
        const response = processQuery(query);
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
