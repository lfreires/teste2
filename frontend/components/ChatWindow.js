import { useRef, useEffect } from 'react';
import ChatMessage from './ChatMessage';

export default function ChatWindow({ mensagens, digitando }) {
  const chatRef = useRef(null);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [mensagens, digitando]);

  return (
    <div
      ref={chatRef}
      className="chat-window"
      style={{
        height: '75vh',
        backgroundColor: '#1e1e1e',
        borderRadius: '12px',
        padding: 20,
        boxShadow: '0 4px 20px rgba(0,0,0,0.25)',
        display: 'flex',
        flexDirection: 'column',
        gap: 10
      }}
    >
      {mensagens.map((msg, idx) => (
        <ChatMessage key={idx} text={msg.text} type={msg.type} />
      ))}

      {digitando && (
        <div style={{
          display: 'flex',
          justifyContent: 'flex-start'
        }}>
          <div style={{
            background: '#e5e7eb',
            padding: '10px 15px',
            borderRadius: '18px',
            display: 'flex',
            gap: 5,
            alignItems: 'center'
          }}>
            <div className="dot" />
            <div className="dot" />
            <div className="dot" />
          </div>
        </div>
      )}
    </div>
  );
}
