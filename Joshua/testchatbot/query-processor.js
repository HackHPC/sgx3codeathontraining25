export const processUserQuery = (query, resourceData) => {
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
};
