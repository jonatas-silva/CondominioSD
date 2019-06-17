from constCS2 import *
import zmq
import ast # biblioteca usada para converter String em um Dicionario
from random import * # randint(0,9) , random.choice('abc') # Gera numeros aleatorios inteiros
# from threading import Thread

context = zmq.Context()
p = "tcp://"+ HOST +":"+ PORT2 # how and where to connect
s  = context.socket(zmq.REP)    # create reply socket
s.bind(p)                      # bind socket to address

andar1_MAX = 15 # quantidade maximo de pessoas dentro do andar
lista_espera_MAX = 10 # quantidade maxima de pessoas na lista de espera do andar
id_andar = "andar 1" # identificador do andar
id_andar2 = "Andar 1" # identificador do andar

lista_atual = [] # lista de pessoas que estao no andar
lista_espera = [] # lista de pessoas na espera

# remove alguma(s) pessoa(s) do andar (aleatoriamente)
def funcao_remove():   
  for i in range(randint(1, 2)):
    if len(lista_atual) > 0:
      print "\n- Saiu um " + lista_atual.pop(0) + " do " + id_andar + "\n"
      print id_andar2 + " : [" + str(len(lista_atual)) + "] pessoa(s) --- Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
      verifica_pessoas_fila_espera()

# verificar se nao existe pessoas na lista de espera do andar
def verifica_pessoas_fila_espera():
  if len(lista_espera) > 0 and len(lista_atual) < andar1_MAX:
    temp = lista_espera.pop(0) # remove o primeiro da lista_espera e ...
    lista_atual.append(temp) # ... o adiciona em ultimo na lista_atual
    print "\n+ Um " + temp + " saiu da lista de espera e entrou no " + id_andar + "\n" ###
    print id_andar2 + " : [" + str(len(lista_atual)) + "] pessoa(s) --- Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
    # lista_espera.append(message["id"]) # adiciona no fim da lista de espera a pessoa recebida por ultimo pelo predio
    # return len(lista_espera)
    # s.send("test")

while True:

  while len(lista_espera) > 0 and len(lista_atual) < andar1_MAX:
    verifica_pessoas_fila_espera()

  # recebe uma nova pessoa do predio 1
  message = ast.literal_eval(s.recv())    # converte uma string em dicionario
  # print "Msg recebida: " + message["id"]

  # caso tenha mais que 5 pessoas no andar, chama a funcao (aleatoriamente) e remove algumas pessoas
  if len(lista_atual) > 5 and bool(getrandbits(1)) == True:
    funcao_remove()   # chama a funcao remove

  # caso ainda tenha vaga no andar e o tamanho da lista de espera seja menor que lista_espera_MAX
  if len(lista_atual) < andar1_MAX and len(lista_espera) < lista_espera_MAX:

    # verificando se a pessoa queria vir realmente para este andar
    if message["andar"] == "andar1":
      lista_atual.append(message["id"])
      print "\n> Entrou um " + message["id"] + " no " + id_andar + "\n"
      print id_andar2 + " : [" + str(len(lista_atual)) + "] pessoa(s) --- Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
      s.send("ok") # retorna "ok" para o predio, caso consiga adicionar a pessoa no andar
    else:
      print "nao sou o andar correto\n" # nunca deve ocorrer
      continue

  else:
    if len(lista_espera) >= lista_espera_MAX:
      print "\n*** Lista de espera do " + id_andar + " andar esta cheia ***\n"
      s.send("listacheia")
      # caso tenha mais que 5 pessoas no andar, chama a funcao (aleatoriamente) e remove algumas pessoas
      if len(lista_atual) > 5 and bool(getrandbits(1)) == True:
        funcao_remove()   # chama a funcao remove
      continue
      
    lista_espera.append(message["id"])
    print id_andar2 + " : [" + str(len(lista_atual)) + "] pessoa(s) --- Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
    s.send("ok") # retorna "ok" para o predio, caso consiga adicionar a pessoa no andar


# msg = s.recv()
# s.send(msg + "*")