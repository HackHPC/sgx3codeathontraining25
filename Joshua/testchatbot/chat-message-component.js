import React from 'react';

const ChatMessage = ({ message, type }) => {
    return (
        <div 
            className={`message ${type === 'user' ? 'user-message' : 'bot-message'}`}
        >
            {message}
        </div>
    );
};

export default ChatMessage;
