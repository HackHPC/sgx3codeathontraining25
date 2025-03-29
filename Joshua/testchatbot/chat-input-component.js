import React, { useState } from 'react';

const ChatInput = ({ onSendMessage }) => {
    const [input, setInput] = useState('');

    const handleSend = () => {
        if (input.trim()) {
            onSendMessage(input);
            setInput('');
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    };

    return (
        <div className="flex space-x-2">
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about science gateways..."
                className="flex-grow p-2 border rounded"
            />
            <button 
                onClick={handleSend}
                className="bg-blue-500 text-white px-4 py-2 rounded"
            >
                Send
            </button>
        </div>
    );
};

export default ChatInput;
