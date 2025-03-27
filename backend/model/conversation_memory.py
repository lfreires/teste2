class ConversadorTemporario:
    def __init__(self, limite=5):
        self.historico = []
        self.limite = limite

    def adicionar(self, pergunta, resposta):
        self.historico.append({
            "pergunta": pergunta,
            "resposta": resposta
        })

        # Mantém só os últimos N pares
        if len(self.historico) > self.limite:
            self.historico.pop(0)

    def limpar(self):
        self.historico = []

    def obter(self):
        return self.historico.copy()  # evita mutação externa
