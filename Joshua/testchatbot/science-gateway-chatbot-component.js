import React, { useState, useEffect } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import { processUserQuery } from '../utils/queryProcessor';
import scienceGatewaysData from '../data/scienceGateways.json';

const ScienceGatewayChatbot = () => {
    const [messages, setMessages] = useState([
        {
            id: 'welcome',
            type: 'bot',
            content: 'Welcome to the Science Gateway Research Assistant! I can help you explore various science gateways and research tools. What would you like to know?'
        }
    ]);

    const handleSendMessage = (input) => {
        // Add user message
        const userMessage = {
            id: `user-${Date.now()}`,
            type: 'user',
            content: input
        };

        // Process response
        const botResponse = {
            id: `bot-${Date.now()}`,
            type: 'bot',
            content: processUserQuery(input, scienceGatewaysData)
        };

        setMessages(prev => [...prev, userMessage, botResponse]);
    };

    return (
        <div className="chat-container p-4">
            <div className="chat-messages mb-4 h-96 overflow-y-auto">
                {messages.map(message => (
                    <ChatMessage 
                        key={message.id} 
                        message={message.content} 
                        type={message.type} 
                    />
                ))}
            </div>
            <ChatInput onSendMessage={handleSendMessage} />
        </div>
    );
};

export default ScienceGatewayChatbot;
