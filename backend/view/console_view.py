class ConsoleView:
    def __init__(self, controller):
        self.controller = controller

    def iniciar_chat(self):
        print("✅ Sistema carregado! Digite uma pergunta (ou 'sair'):")

        while True:
            pergunta = input("\n❓ Sua pergunta: ")
            if pergunta.lower() == 'sair':
                break

            resposta = self.controller.responder(pergunta)
            print("\n🧠 Resposta do ChatGPT:\n")
            print(resposta)
