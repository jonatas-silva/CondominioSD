import zmq
from constCS import * # armazena todas informacoes
from random import * # randint(0,9) , random.choice('abc') # Gera numeros aleatorios inteiros
import time

context = zmq.Context()
p = "tcp://"+ HOST +":"+ PORT1 # how and where to connect
s  = context.socket(zmq.REQ)    # cria socket de requisicao
s.connect(p)                   # block until connected

condominio_MAX = 200; # capacidade maximo no condominio
lista_espera_MAX = 25

frequentadores = ["visitante", "funcionario do condominio", "funcionario de empresa"] # lista
frequentadores_dic = {1 : "visitante", 2 : "funcionario do condominio", 3 : "funcionario de empresa"} # dicionario
predios = {1 : "predio1", 2 : "predio2", 3 : "predio3", 4 : "predio4"}
andares = {1 : "andar1", 2 : "andar2", 3 : "andar3", 4 : "andar4"}

# lista de pesoas na espera
lista_atual = [] # lista de pessoas que estao no condominio
lista_espera = [] # lista de pessoas na espera

# controle de acesso
def controle_acesso(id):
    if id == "visitante":
        acesso = [randint(1,4)]
    elif id == "funcionario do condominio":
        acesso = [1, 2, 3, 4]
    else:
        acesso = [randint(1,4), randint(1,4)]
        while acesso[0] == acesso[1]:
            acesso = [randint(1,4), randint(1,4)]
    return acesso

# analisa a msg do andar sobre a pessoa
def resposta_predio(exemplo, msg):
    if msg == 'ok':
        lista_atual.append(exemplo) # adiciona uma pessoa no condominio
        print "\n> Entrou um " + exemplo["id"] + " no condominio\n"
        print "Condominio : [" + str(len(lista_atual)) + "] pessoa(s) --- Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
        # print msg
    elif msg == "erro":
        print "O " + exemplo["id"] + " nao possui acesso ao predio interessado!\n"
    elif msg == "listacheia":
        lista_espera.append(exemplo)
        print "Condominio : [" + str(len(lista_atual)) + "] pessoa(s) --- 2 Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
    elif msg == "removido": ### 
        lista_atual.pop(0)
    else:
        print "erro_app\n"

# verificar se nao existe pessoas na lista de espera do condominio
def verifica_pessoas_fila_espera():
  if len(lista_espera) > 0 and len(lista_atual) < condominio_MAX:
    temp = lista_espera.pop(0) # remove o primeiro da lista_espera e ...
    lista_atual.append(temp) # ... o adiciona em ultimo na lista_atual
    print "\n+ Um " + temp["id"] + " saiu da lista de espera e entrou no condominio\n" ###
    print "Condominio : [" + str(len(lista_atual)) + "] pessoa(s) --- 3 Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
    return len(lista_espera)

# funcao principal
def main(exemplo, casos_teste):
    for i in range(casos_teste):

        time.sleep(1)
        if len(lista_atual) < condominio_MAX and len(lista_espera) < lista_espera_MAX:

            while len(lista_espera) > 0 and len(lista_atual) < condominio_MAX: ### talvez inutil
                verifica_pessoas_fila_espera()

            s.send(str(exemplo))
            msg = s.recv()

            resposta_predio(exemplo, msg) # verifica se nao existe pessoas na lista de espera do condominio
        else:
            if len(lista_espera) >= lista_espera_MAX:
                print "\n*** Fila do condominio esta cheia ***\n"
                continue
            lista_espera.append(exemplo)
            print "Condominio : [" + str(len(lista_atual)) + "] pessoa(s) --- 4 Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"


controle = 1
while controle != 0:
    op = input ("\n** BEM VINDO AO SIMULADOR DE CONDOMINIO DE EMPRESAS **\n\n\t1 - Teste automatizado\n\t2 - Inserir uma pessoa manualmente\n\t0 - SAIR\n>: ")
    if op == 1: # teste automatizado
        casos_teste = input ("\nInforme a quantidade de instancias (aleatorias) de entrada\n>: ")

        id = choice(frequentadores) # definindo (aleatoriamente) uma pessoa para usar no exemplo de instancia
        acesso = controle_acesso(id) # controle de acesso

        # exemplo de instancia de Pessoa
        pessoa = {"id" : str(id), "predio" : "predio1", "andar" : "andar1", "acesso" : str(acesso)}

        main(pessoa, casos_teste)
    elif op == 2: # inserir uma pessoa manualmente
        id_op = input ("Id -> 1 - visitante\t2 - funcionario do condominio\t3 - funcionario de empresa\n>: ")
        id = frequentadores_dic[id_op]
        predio_op = input ("predio -> 1 - predio1\t2 - predio2\t3 - predio3\t4 - predio4\n>: ")
        predio = predios[predio_op]
        andar_op = input("andar -> 1 - andar1\t2 - andar2\t3 - andar3\t4 - andar4\n>: ")
        andar = andares[andar_op]
        # acesso = input("politica de acesso -> 1 - visitante\t2 - fucionario do condominio\t3 - funcionario de empresa\n>: ")

        # exemplo de uma instancia de Pessoa
        pessoa = {"id" : str(id), "predio" : str(predio), "andar" : str(andar), "acesso" : str(id)}
        main(pessoa, 1)
    elif op == 0: # sair
        controle = 0
    else:
        print "\nComando invalido, tente novamente!\n"
    

