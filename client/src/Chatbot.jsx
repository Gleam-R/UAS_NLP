import React, { useState } from "react";
import "./App.css"; // Mengimpor CSS untuk styling

const Chatbot = () => {
    const [messages, setMessages] = useState([]); // Menyimpan pesan dalam state
    const [userInput, setUserInput] = useState(""); // Menyimpan input user
    const [isLoading, setIsLoading] = useState(false); // State untuk loading

    const sendMessage = async () => {
        if (userInput.trim()) {
            // Menambahkan pesan user ke dalam chat hanya sekali
            setMessages((prevMessages) => [
                ...prevMessages,
                { text: userInput, sender: "user" },
            ]);

            setIsLoading(true); // Set loading state menjadi true sebelum mendapatkan response

            try {
                // Mengirim permintaan ke backend Flask
                const response = await fetch("http://localhost:5000/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ question: userInput }), // Mengirim data input ke backend
                });

                const data = await response.json(); // Mengambil data respons dari server

                // Menambahkan respons chatbot ke dalam chat hanya sekali
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { text: data.response, sender: "bot" },
                ]);
            } catch (error) {
                console.error("Error fetching response:", error);
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { text: "Maaf, terjadi kesalahan.", sender: "bot" },
                ]);
            } finally {
                setIsLoading(false); // Set loading state menjadi false setelah mendapatkan response
            }

            // Reset input field
            setUserInput("");
        }
    };


    return (
        <div className="chat-container">
            <div className="chat-box">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={`message ${message.sender === "bot" ? "bot" : "user"}`}
                    >
                        {message.text}
                    </div>
                ))}

                {isLoading && (
                    <div className="message bot">Sedang memproses...</div> // Menampilkan loading saat chatbot sedang memproses
                )}
            </div>

            <div className="input-container">
                <input
                    type="text"
                    placeholder="Tanya sesuatu..."
                    value={userInput}
                    onChange={(e) => setUserInput(e.target.value)} // Update input
                />
                <button onClick={sendMessage}>Kirim</button>
            </div>
        </div>
    );
};

export default Chatbot;
