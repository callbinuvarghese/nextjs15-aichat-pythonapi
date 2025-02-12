"use client";

import { useState, useEffect, useRef } from 'react';
import { Chat } from "@/components/ui/chat";

export function ChatDemo() {
    const [messages, setMessages] = useState([]);
    const [userInput, setUserInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const messageContainerRef = useRef(null); // Ref for the message container

    useEffect(() => {
        // Scroll to bottom when new messages are added
        if (messageContainerRef.current) {
        messageContainerRef.current.scrollTop = messageContainerRef.current.scrollHeight;
        }
    }, [messages]); // Run effect when messages change

    const getChatCompletion = async (currentMessages) => {
        setIsLoading(true);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ messages: currentMessages }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error("Error from API:", errorData);
                setMessages(prevMessages => [...prevMessages, { role: 'assistant', content: "Error: " + (errorData?.error || "An error occurred") }]);
                setIsLoading(false);
                return;
            }

            const contentType = response.headers.get('Content-Type'); // Get Content-Type *first*
            const contentTypeMediaType = contentType?.split(';')[0]; // Split by ';' and take the first part
            console.log('contentTypeMediaType Type:', contentTypeMediaType);
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let fullResponse = "";

            while (true) {
                const { done, value } = await reader.read();
                if (done) {
                    break;
                }

                const chunk = decoder.decode(value);
                fullResponse += chunk;

                setMessages(prevMessages => {
                    const newMessages = [...prevMessages];
                    const lastMessageIndex = newMessages.length - 1;

                    if (lastMessageIndex >= 0 && newMessages[lastMessageIndex].role === 'assistant') {
                        // Correctly update the LAST message's content
                        newMessages[lastMessageIndex] = { ...newMessages[lastMessageIndex], content: fullResponse, contentType: contentTypeMediaType};
                    } else {
                        // Correctly ADD a new assistant message
                        newMessages.push({ role: 'assistant', content: chunk, contentType: contentTypeMediaType});
                        fullResponse = chunk; // Reset fullResponse if a new message is added
                    }

                    console.log("Current Messages:", newMessages); // Log the updated messages

                    return newMessages; // Return the updated array
                });
            }

        } catch (error) {
            console.error("Fetch Error:", error);
            setMessages(prevMessages => [...prevMessages, { role: 'assistant', content: "Error: " + error.message }]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (userInput.trim() !== "") {
            setMessages(prevMessages => [...prevMessages, { role: 'user', content: userInput }]); // Update with user message
            setUserInput("");
            await getChatCompletion([...messages, { role: 'user', content: userInput }]); // Send updated messages
        }
    };

    return (
        <div className="flex h-[500px] w-full">
            <Chat
                className="grow"
                messages={messages}
                handleSubmit={handleSubmit}
                input={userInput}
                handleInputChange={e => setUserInput(e.target.value)}
                isGenerating={isLoading}
                suggestions={[ /* ... */ ]}
            />
        </div>
    );
}

export default ChatDemo;