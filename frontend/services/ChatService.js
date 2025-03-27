import axios from 'axios';

class ChatService {
  constructor(baseURL) {
    this.api = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  async enviarMensagem(mensagem) {
    try {
      const response = await this.api.post(
        '/perguntar?pergunta=' + encodeURIComponent(mensagem)
      );
      return response.data.resposta;
    } catch (error) {
      if (error.response) {
        console.error("Erro na resposta do servidor:", error.response);
        return "💥 O servidor respondeu com erro. Tente novamente.";
      } else if (error.request) {
        console.error("Servidor não respondeu:", error.request);
        return "⚠️ Sem conexão ...";
      } else {
        console.error("Erro desconhecido:", error.message);
        return "😵 Ocorreu um erro inesperado. Tente novamente.";
      }
    }
  }
}

const chatService = new ChatService('http://localhost:8000');
export default chatService;
