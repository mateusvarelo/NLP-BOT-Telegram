class Token:

    def get_token(self):
            file= 'token-telegram.txt'
            arquivo = open(file, 'r',encoding="utf-8")
            token_telegram = arquivo.read()
            
            return token_telegram

