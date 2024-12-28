import React, { useState } from "react";
import "./App.css";

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [userInput, setUserInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const sendMessage = async () => {
        if (userInput.trim()) {
            setMessages((prevMessages) => [
                ...prevMessages,
                { text: userInput, sender: "user" },
            ]);

            setIsLoading(true);

            try {
                const response = await fetch("http://localhost:5000/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ question: userInput }),
                });

                const data = await response.json();

                setMessages((prevMessages) => [
                    ...prevMessages,
                    { text: data.response, sender: "bot" },
                ]);
            } catch (error) {
                console.error("Error fetching response:", error);
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { text: "Sorry, something went wrong.", sender: "bot" },
                ]);
            } finally {
                setIsLoading(false);
            }

            setUserInput("");
        }
    };

    return (
        <div className="chatbot-container">
            <div className="chatbot-header">
                <h1>Chatbot</h1>
            </div>
            <div className="chat-box">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`message-wrapper ${message.sender === "bot" ? "bot" : "user"
                            }`}
                    >
                        <img
                            src={
                                message.sender === "bot"
                                    ? "/vite.svg"
                                    : "/ProfilePicture.jpeg"
                            }
                            alt={`${message.sender}-avatar`}
                            className="avatar"
                        />
                        <div className="message">{message.text}</div>
                    </div>
                ))}
                {isLoading && (
                    <div className="message-wrapper bot">
                        <img
                            src="/vite.svg"
                            alt="bot-avatar"
                            className="avatar"
                        />
                        <div className="message loading">...</div>
                    </div>
                )}
            </div>
            <div className="input-container">
                <input
                    type="text"
                    placeholder="Ask something..."
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)}
                    onKeyPress={(e) => e.key === "Enter" && sendMessage()}
                />
                <button onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
};

export default Chatbot;
