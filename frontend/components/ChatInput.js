export default function ChatInput({ mensagem, setMensagem, onEnviar }) {
    const handleKeyDown = (e) => {
      if (e.key === 'Enter') onEnviar();
    };
  
    return (
      <div style={{
        marginTop: 20,
        display: 'flex',
        borderRadius: '999px',
      }}>
        <input
          type="text"
          value={mensagem}
          onChange={(e) => setMensagem(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Digite sua mensagem..."
          style={{
            flex: 1,
            padding: '12px',
            borderRadius: '999px',
            border: 'none',
            outline: 'none',
            fontSize: 16,
            background: '#2a2a2a',
            color: '#fff'
          }}
        />
        <button
          onClick={onEnviar}
          style={{
            marginLeft: 10,
            padding: '12px 20px',
            borderRadius: '999px',
            border: 'none',
            background: '#10a37f',
            color: 'white',
            fontWeight: 'bold',
            cursor: 'pointer'
          }}
        >
          Enviar
        </button>
      </div>
    );
  }
  