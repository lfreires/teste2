import { useState, useEffect } from 'react';
import ChatWindow from '../components/ChatWindow';
import ChatInput from '../components/ChatInput';
import chatService from '../services/ChatService';

export default function Home() {
  const [mensagem, setMensagem] = useState('');
  const [mensagens, setMensagens] = useState([]);
  const [digitando, setDigitando] = useState(false);

  useEffect(() => {
    const mensagemInicial = {
      text: "👋 Olá! Sou seu assistente. Envie uma pergunta sobre o conteúdo que você está estudando 📚",
      type: "bot"
    };
    setMensagens([mensagemInicial]);
  }, []);

  const handleEnviar = async () => {
    if (!mensagem.trim()) return;
  
    const novaMensagem = { text: mensagem, type: 'user' };
    setMensagens((msgs) => [...msgs, novaMensagem]);
    setMensagem('');
    setDigitando(true);
  
    try {
      const resposta = await chatService.enviarMensagem(mensagem);
  
      setMensagens((msgs) => [
        ...msgs,
        { text: resposta, type: 'bot' }
      ]);
    } catch (error) {
      console.error("Erro ao enviar mensagem:", error);
  
      setMensagens((msgs) => [
        ...msgs,
        {
          text: "Opa! Tivemos um problema para responder agora. Tente novamente em instantes.",
          type: "erro"
        }
      ]);
    } finally {
      setDigitando(false);
    }
  };

  return (
    <div style={{
      height: '100vh', 
      backgroundColor: '#121212',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
    }}>
      <div style={{
        width: '100%',
        maxWidth: 800,
        display: 'flex',
        flexDirection: 'column',
        gap: 20,
        padding: 20,
        boxSizing: 'border-box'
      }}>
        <ChatWindow mensagens={mensagens} digitando={digitando} />
        <ChatInput
          mensagem={mensagem}
          setMensagem={setMensagem}
          onEnviar={handleEnviar}
        />
      </div>
    </div>
  );
}
