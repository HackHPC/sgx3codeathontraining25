import React,

{useState}
from

"react";

const
Chatbot = () = > {
    const[messages, setMessages] = useState([]);
const[input, setInput] = useState("");

const
sendMessage = async () = > {
if (!input.trim()) return;

const
userMessage = {sender: "user", text: input};
setMessages([...messages, userMessage]);
setInput("");

try {
const response = await fetch("http://127.0.0.1:5000/query", {
method: "POST",
headers: {"Content-Type": "application/json"},
body: JSON.stringify({message: input})
});
const
data = await response.json();

const
botMessages = data.map(res= > ({sender: "bot", text: `${res.name}: ${res.abstract} \n More: ${res.site_url}`}));
setMessages([...messages, userMessage, ...botMessages]);
} catch(error)
{
    console.error("Error fetching response:", error);
}
};

return (
    < div className="flex flex-col h-screen max-w-md mx-auto p-4 border rounded-lg shadow-lg" >
    < div className="flex-1 overflow-y-auto mb-4" >
    {messages.map((msg, index) = > (
    < div key={index} className={`mb-2 p-2 rounded-lg ${msg.sender == = "user" ? "bg-blue-500 text-white self-end": "bg-gray-200 text-black self-start"}`} >
    {msg.text}
    < / div >
))}
< / div >
    < div
className = "flex gap-2" >
            < input
type = "text"
className = "flex-1 p-2 border rounded"
placeholder = "Ask me about Science Gateways..."
value = {input}
onChange = {(e) = > setInput(e.target.value)}
onKeyPress = {(e) = > e.key == = "Enter" & & sendMessage()}
/ >
< button
onClick = {sendMessage}
className = "bg-blue-500 text-white p-2 rounded" > Send < / button >
                                                            < / div >
                                                                < / div >
);
};

export
default
Chatbot;
