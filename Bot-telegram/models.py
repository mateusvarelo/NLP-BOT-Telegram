import joblib
import nltk
from nltk import tokenize
import unidecode
from string import punctuation
import sklearn.externals
# nltk.download('stopwords')
# nltk.download('rslp')

file_modelo = 'modelo_analise_sentimento.pkl'

file_voca = 'modelo_analise_sentimento_vector.pkl'
# identificando as palavras irrelevantes (stop words)
palavras_irrelevantes = nltk.corpus.stopwords.words('portuguese')

# listando a pontuação
pontuacao = list()
for ponto in punctuation:
    pontuacao.append(ponto) 
    
palavras_irrelevantes_e_pontuacao = pontuacao + palavras_irrelevantes

# adicionando casos onde as aspas (simples e duplas) estão no final da frase
palavras_irrelevantes_e_pontuacao.append('".')
palavras_irrelevantes_e_pontuacao.append("'.")
palavras_irrelevantes_e_pontuacao.append('...')

# removendo os acentos
palavras_irrelevantes_e_pontuacao_sem_acento = [unidecode.unidecode(sw) for sw in palavras_irrelevantes_e_pontuacao]

# tokenizador de frases
punct_tokenizer = tokenize.WordPunctTokenizer()

# calculador do stemm das palavras
stemmer = nltk.RSLPStemmer()


def get_modelo_vecto():
        modelo_load  = joblib.load(file_modelo)
        vetor =joblib.load(file_voca)
        return modelo_load , vetor
def get_sentindo(modelo, vetorizador, opiniao):
        nova_opiniao = list()
        palavras_opiniao = tokenize.WordPunctTokenizer().tokenize(unidecode.unidecode(opiniao.lower()))
        for palavra in palavras_opiniao:
            if palavra not in palavras_irrelevantes_e_pontuacao_sem_acento:
                nova_opiniao.append(stemmer.stem(palavra))
        opiniao_filtrada = ' '.join(nova_opiniao)

    
        big_bag_of_words = vetorizador.transform([opiniao_filtrada])
    
        return 'positivo :)' if  (modelo.predict(big_bag_of_words)[0] == 1) else 'negativo (:'

