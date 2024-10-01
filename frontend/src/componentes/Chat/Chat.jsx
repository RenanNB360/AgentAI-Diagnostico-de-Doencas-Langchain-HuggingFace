import React, { useState, useEffect, useRef } from 'react';
import './Chat.css';
import { TbNurse } from "react-icons/tb";
import { IoPersonCircleOutline } from "react-icons/io5";
import { useNavigate } from 'react-router-dom'; 

const Chat = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [ws, setWs] = useState(null);
    const chatLogRef = useRef(null);
    const [chatEnded, setChatEnded] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        const socket = new WebSocket('ws://127.0.0.1:8000/ws');

        socket.onopen = () => {
            console.log('Conectado ao WebSocket');
        };

        socket.onmessage = (event) => {
            setMessages(prevMessages => [...prevMessages, { sender: 'nurse', text: event.data }]);
        };

        socket.onclose = () => {
            console.log('Conexão com WebSocket fechada');
            setChatEnded(true);
        };

        setWs(socket);

        return () => {
            socket.close();
        };
    }, []);

    const sendMessage = () => {
        if (ws && input) {
            ws.send(input);
            setMessages(prevMessages => [...prevMessages, { sender: 'user', text: input }]);
            setInput('');
        }
    };

    useEffect(() => {
        if (chatLogRef.current) {
            chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
        }
    }, [messages]);

    const goToRegister = () => {
        navigate('/register'); 
    };

    return (
        <div>
            <div className='chat-log' ref={chatLogRef}>
                {messages.map((msg, index) => (
                    <div key={index} className={`chat-message ${msg.sender}`}>
                        <div className='chat-message-center'>
                            <div className={`avatar ${msg.sender}`}>
                                {msg.sender === 'nurse' ? <TbNurse className='icon' /> : <IoPersonCircleOutline className='icon' />}
                            </div>
                            <div className='message'>
                                <p>{msg.text}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
            <div className='chat-input-holder'>
                <textarea 
                    rows="1"
                    className='chat-input-text'
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                ></textarea>
                <button onClick={sendMessage}>Enviar</button>
            </div>
            {chatEnded && (
                <div className="appointment-link">
                    <button onClick={goToRegister}>Make an Appointment</button>
                </div>
            )}
        </div>
    );
};

export default Chat;
