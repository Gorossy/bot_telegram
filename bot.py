from telegram import update
from telegram.error import TimedOut
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from bs4 import BeautifulSoup
import requests
import re
import random
import networkx as nx
import random
import matplotlib.pyplot as plt
from telegram import ChatAction
INPUT_TEXT=0
def iniciar(update, context):
    update.message.reply_text('Hola! este es el bot de David Maldonado, Emanuel Escobar y Robin Restrepo')
    update.message.reply_text('Digita /help para conocer mis capacidades!')
def ayuda(update, context):
    update.message.reply_text('Que bien que pueda ayudarte, tengo cuatro funciones principales: ')
    update.message.reply_text('/pol ,Este comando recibe los coeficientes de un polinomio para retornar la forma de su solucion')
    update.message.reply_text('/pol2 ,Este comando recibe los coeficientes de un polinomio y sus casos base para retornar la expresion con valores de sus constantes y su relacion de recurrencia')
    update.message.reply_text('/markov ,Este comando retorna un texto ficticio dado un url de una pagina web')
    update.message.reply_text('/graph ,Este comando recibe vertice, numero de aristas, y maximo de aristas en un vertice para retornar la imagen de un grafo')
def polinomio(update, context):
    update.message.reply_text('Digite su polinomio')
    return INPUT_TEXT
def convertir():
    pass
def retornar_pol():
    pass
def obtenerurl(update, context):
    update.message.reply_text('Digite la url')
    return INPUT_TEXT
def funcion(update, context):
    pol = update.message.text
    nuevo = convertir()
    retornar_pol(nuevo)
    return ConversationHandler.END

def Clean(text: str):
    text = re.sub(r"\\n", "", text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'[0-9]+', '', text)
    text = re.sub(' +', ' ', text)
    return text
def markov(dic,letras):
    frecuencias = []
    for key in dic.keys():
        faq = float(str(dic.get(key)).replace("[", "").replace("]", ""))
        frecuencias.append(faq)
    final = []
    for recorrido in letras:
        ranNum = random.random()
        prob = min(frecuencias, key=lambda x:abs(x-ranNum))
        for cadena in dic.keys():
            if prob == float(str(dic.get(cadena)).replace("[", "").replace("]", "")):
                final.append(str(cadena))
    
    final = str(final)
    return Clean(final)

def scraping(update, context):
    url = update.message.text
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    contenido = soup.html
    text = []
    for string in contenido.strings:
        text.append(string)
    text = str(text)
    text = Clean(text)
    print(text)
    letras = list(text)
    dic = {}
    for letra in letras:
        if letra not in dic.keys():
            dic[letra] = 1
        else:
            dic[letra] += 1
    freqa = 0
    for llave in dic.keys():
        freq = dic[llave]/len(letras)
        freqa += freq
        dic[llave] = [freqa]
    textourl= markov(dic,letras)
    update.message.reply_text(textourl)
    return ConversationHandler.END
def sendgraph(chat,filename):
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    chat.send_photo(
        photo=open(filename,'rb')
    )
def graph(update, context):
    update.message.reply_text('Digite el grafo de esta forma V,E,K (Tenga en cuenta que V tiene que ser mayor que k)')
    return INPUT_TEXT
def infograph(update, context):
    datos = update.message.text
    grafo=datos.split(',')
    v=int(grafo[0])
    e=int(grafo[1])
    k=int(grafo[2])
    if (v*k)/2 >= e and v>k:
        filename = create(v,e,k)
        chat = update.message.chat
        sendgraph(chat,filename)
        return ConversationHandler.END
    else:
        update.message.reply_text('Se digito un grafo incorrecto')

def Save(graph):
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])
    G=nx.Graph()

    for node in nodes:
        G.add_node(node)
        
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    pos = nx.shell_layout(G)
    nx.draw(G, pos)

    plt.savefig("grafo.png")
    return 'grafo.png'

def create(n,e,k):
    graph = []
    nodes=[] 
    for node in range(1,n):
        nodes.append(node)                     
    while len(graph) < e:  
        edge = random.randint(0,k-1)
        nodeA = random.choice(nodes) 
        
        if tam(nodeA,graph) <=k and (nodeA,edge) not in graph and (edge,nodeA) not in graph:
            graph.append((nodeA,edge))
        elif tam(nodeA,graph) > k: print(f"{nodeA}excedio el peso")
    url = Save(graph)
    return url

def tam(node,graph):
    cont=0
    for edge in graph:
        if node in edge:
            cont+=1
            
    return cont 


if __name__ == '__main__':
    updater = Updater("2096487868:AAHlgfQwT1rjGv4J3UU41B7FhByM4IzVKUQ",use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',iniciar))
    dp.add_handler(CommandHandler('help',ayuda))
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('pol',polinomio)
        ],
        states={INPUT_TEXT:[MessageHandler(Filters.text, funcion)]},
        fallbacks=[]

    ))
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('markov',obtenerurl)
        ],
        states={INPUT_TEXT:[MessageHandler(Filters.text, scraping)]},
        fallbacks=[]

    ))
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('graph',graph)
        ],
        states={INPUT_TEXT:[MessageHandler(Filters.text, infograph)]},
        fallbacks=[]

    ))
    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('pol2',polinomio)
        ],
        states={INPUT_TEXT:[MessageHandler(Filters.text, funcion)]},
        fallbacks=[]

    ))
updater.start_polling()
updater.idle()