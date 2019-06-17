from constCS import *
import zmq
import ast # biblioteca usada para converter String em um Dicionario
from random import * # randint(0,9) , random.choice('abc') # Gera numeros aleatorios inteiros

context = zmq.Context()
p1 = "tcp://"+ HOST +":"+ PORT1 # how and where to connect
a1 = "tcp://"+ HOST2 +":"+ PORT2 # how and where to connect
s  = context.socket(zmq.REP)    # create reply socket
r1 = context.socket(zmq.REQ)     # cria socket de requisicao
s.bind(p1)                      # bind socket to address
r1.connect(a1)                   # block until connected

predio_MAX = 50
lista_espera_MAX = 15

# lista de pesoas na espera
lista_atual = [] # lista de pessoas que estao no andar
lista_espera = [] # lista de pessoas na espera

# remove alguma(s) pessoa(s) do predio (aleatoriamente)
def funcao_remove():   
  for i in range(randint(1, 2)):
    if len(lista_atual) > 0:
      print "\n- Saiu um " + (lista_atual.pop(0))["id"] + " do predio\n"
      print "Predio 1 : [" + str(len(lista_atual)) + "] pessoa(s) --- Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
      verifica_pessoas_fila_espera()

# analisa a msg do andar sobre a pessoa
def resposta_andar(msg):
  if msg == "ok": # pessoa entrou no andar
    lista_atual.append(message)
    print "\n> Entrou um " + message["id"] + " no predio\n"
    print "Predio 1 : [" + str(len(lista_atual)) + "] pessoa(s) --- 2 Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
    s.send("ok") # retorna "ok" para o condominio, caso consiga adicionar a pessoa no predio
  elif msg == "listacheia": # pessoa nao entrou no andar pois a lista de espera estava cheia, entao adiciona na lista de espera do predio
    s.send("listacheia")
    # lista_atual.append(message)
    # print "Predio 1 : [" + str(len(lista_atual)) + "] pessoa(s) --- 3 Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
  else:
    print "erro_predio\n"

def funcao_verifica_predio(message):
  # verificando se a pessoa queria vir realmente para este predio
  if message["predio"] == "predio1":

    # mandar a pessoa para o andar 1
    if message["andar"] == "andar1":
      r1.send(str(message))
    msg = r1.recv()
    return msg # string de retorno do andar 1
  else:
      print "nao sou o predio correto\n" # nunca deve ocorrer
      s.send("erro")

# verificar se nao existe pessoa(s) na lista de espera do predio
def verifica_pessoas_fila_espera():
  if len(lista_espera) > 0 and len(lista_atual) < predio_MAX:
    temp = lista_espera.pop(0) # remove a primeira pessoa da lista_espera
    msg = funcao_verifica_predio(temp) # recebe a msg do andar sobre a pessoa
    if msg == "ok": # pessoa entrou no andar
      lista_atual.append(message)
      print "\n+ Um " + temp["id"] + " saiu da lista de espera e entrou no predio\n"
      print "Predio 1 : [" + str(len(lista_atual)) + "] pessoa(s) --- 4 Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
      # s.send("ok") # retorna "ok" para o condominio, caso consiga adicionar a pessoa no predio
    elif msg == "listacheia": # pessoa nao entrou no andar pois a lista de espera estava cheia, entao adiciona na lista de espera do predio
      # s.send("listacheia")
      # lista_espera.append(message)
      # print "Predio 1 : [" + str(len(lista_atual)) + "] pessoa(s) --- 5 Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
      pass

while True:

  while len(lista_espera) > 0 and len(lista_atual) < predio_MAX:
    verifica_pessoas_fila_espera()
      
    # lista_espera.append(message) # adiciona no fim da lista de espera a pessoa recebida por ultimo pelo predio
    # s.send("test")
  
  # recebe uma nova pessoa do condominio
  message = ast.literal_eval(s.recv())    # converte uma string em dicionario
    # print "Msg recebida: " + str(message["id"])
  
  # caso tenha mais que 15 pessoas no predio, chama a funcao (aleatoriamente) e remove algumas pessoas
  if len(lista_atual) > 15 and bool(getrandbits(1)) == True:
    funcao_remove()   # chama a funcao remove

  # caso ainda tenha vaga no andar e o tamanho da lista de espera seja menor que lista_espera_MAX
  if len(lista_atual) < predio_MAX and len(lista_espera) < lista_espera_MAX:
    resposta_andar(funcao_verifica_predio(message))
  else:
    if len(lista_espera) >= lista_espera_MAX:
      print "\n*** Lista de espera do andar esta cheia ***\n"
      s.send("listacheia")
      if len(lista_atual) > 0:
        funcao_remove()   # chama a funcao remove
      continue
    lista_espera.append(message)
    print "Predio 1 : [" + str(len(lista_atual)) + "] pessoa(s) --- 5 Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
    s.send("ok") # retorna "ok" para o condominio, caso consiga adicionar a pessoa no predio



# r.send("Ola")
# msg = r.recv()
# print msg




