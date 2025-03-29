import React, { useState, useEffect, useCallback } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ScrollArea } from '@/components/ui/scroll-area';

const ScienceGatewayChatbot = ({ initialData }) => {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      type: 'system',
      content: 'Welcome to the Science Gateway Research Assistant! I can help you explore various science gateways and research tools. What would you like to know?'
    }
  ]);
  const [input, setInput] = useState('');
  const [resourceData, setResourceData] = useState(initialData || []);

  // Advanced Natural Language Processing (Intent Recognition)
  const processUserQuery = useCallback((query) => {
    const lowercaseQuery = query.toLowerCase();
    
    // Comprehensive intent matching
    const intents = [
      {
        keywords: ['list', 'show', 'all', 'gateways'],
        handler: () => {
          const gatewayList = resourceData.map(gateway => 
            `• ${gateway.name}: ${gateway.abstract.slice(0, 100)}...`
          ).join('\n');
          return `Available Science Gateways:\n${gatewayList}`;
        }
      },
      {
        keywords: ['search', 'find', 'lookup'],
        handler: () => {
          // Try to find gateways matching the query
          const matchedGateways = resourceData.filter(gateway => 
            gateway.name.toLowerCase().includes(lowercaseQuery) ||
            gateway.abstract.toLowerCase().includes(lowercaseQuery) ||
            (gateway.tags && gateway.tags.some(tag => 
              tag.toLowerCase().includes(lowercaseQuery)))
          );
          
          if (matchedGateways.length) {
            return matchedGateways.map(gateway => 
              `Gateway: ${gateway.name}\nDescription: ${gateway.abstract}\nWebsite: ${gateway.site_url}`
            ).join('\n\n');
          }
          return "No gateways found matching your search.";
        }
      },
      {
        keywords: ['domain', 'research', 'type'],
        handler: () => {
          // Extract unique categories/tags
          const domains = [...new Set(
            resourceData.flatMap(gateway => 
              gateway.tags || []
            )
          )];
          return `Research Domains/Tags:\n${domains.join(', ')}`;
        }
      }
    ];

    // Find first matching intent or default response
    const matchedIntent = intents.find(intent => 
      intent.keywords.some(keyword => lowercaseQuery.includes(keyword))
    );

    return matchedIntent 
      ? matchedIntent.handler() 
      : "I can help you list, search, or explore science gateways. Try asking 'list gateways' or 'search for a specific research tool'.";
  }, [resourceData]);

  const handleSendMessage = () => {
    if (!input.trim()) return;

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
      content: processUserQuery(input)
    };

    setMessages(prev => [...prev, userMessage, botResponse]);
    setInput('');
  };

  // Allow sending message with Enter key
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSendMessage();
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-4 bg-white shadow-lg rounded-lg">
      <Card>
        <CardHeader>
          <CardTitle>Science Gateway Research Assistant</CardTitle>
        </CardHeader>
        <CardContent>
          <ScrollArea className="h-96 mb-4 p-4 border rounded">
            {messages.map(message => (
              <div 
                key={message.id} 
                className={`mb-2 p-2 rounded ${
                  message.type === 'user' 
                    ? 'bg-blue-100 text-right' 
                    : 'bg-green-100'
                }`}
              >
                {message.content}
              </div>
            ))}
          </ScrollArea>
          
          <div className="flex space-x-2">
            <Input 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about science gateways..."
              className="flex-grow"
            />
            <Button onClick={handleSendMessage}>Send</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

// Wrapper component to pass JSON data
const ScienceGatewayApp = () => {
  const [gatewayData, setGatewayData] = useState(null);

  useEffect(() => {
    // Assuming the JSON data is passed as a prop or imported
    const data = [
      {
        "name": "Custos Admin Gateway",
        "category": "26 Jun 2024|Science Gateways",
        "site": "https://sciencegateways.org/resources/10214",
        "abstract": "Custos provides security services, including identity management, authorization management, and resource credential management, for science gateways",
        "published_on": "N/A",
        "site_url": "https://portal.usecustos.org/",
        "cite": "(2024), \"Custos Admin Gateway,\" https://sciencegateways.org/resources/10214.",
        "tags": [
            "ACCESS-CI"
        ]
      },
      // ... rest of the data would be here
    ];

    setGatewayData(data);
  }, []);

  if (!gatewayData) {
    return <div>Loading...</div>;
  }

  return <ScienceGatewayChatbot initialData={gatewayData} />;
};

export default ScienceGatewayApp;
