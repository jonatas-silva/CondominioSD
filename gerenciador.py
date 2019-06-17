from constCS import *

# SERVIDOR DO CLIENTE
context = zmq.Context()
p = "tcp://"+ HOST +":"+ PORT1 # how and where to connect
s  = context.socket(zmq.REP)    # cria socket de requisicao
s.bind(p)                   # block until connected

# CLIENTE DO PREDIO 1
p2 = "tcp://"+ HOST +":"+ PORT2
s2  = context.socket(zmq.REQ)
s2.connect(p2)

# SERVIDOR DO PREDIO
p3 = "tcp://"+ HOST +":"+ PORT5 # how and where to connect
s3 = context.socket(zmq.REP)     # cliente do gerenciador
s3.connect(p3)

condominio_MAX = 55; # 180 # capacidade maximo no condominio
lista_espera_MAX = 30 # 10

frequentadores = ["visitante", "funcionario do condominio", "funcionario de empresa"] # lista
frequentadores_dic = {1 : "visitante", 2 : "funcionario do condominio", 3 : "funcionario de empresa"} # dicionario
predios_dic = {"predio1" : "192.168.43.224"}

# lista de pesoas na espera
lista_atual = [] # lista de pessoas que estao no condominio
lista_espera = [] # lista de pessoas na espera

# remove a(s) pessoa(s) do condominio que o andar ja removeu
def funcao_remove(msg2):
  msg2 = msg2.split()
  # 0 = visitante, 1 = func cond, 2 = func empresa
  for i in range(3):
    if int(msg2[i]) > 0:
      for j in range(int(msg2[i])):
        if len(lista_atual) > 0:
          res = lista_atual.remove(frequentadores[i])
          print "\n- Saiu um " + frequentadores[i] + " do condominio\n"
          time.sleep(1)
          print "Condominio : [" + str(len(lista_atual)) + "] pessoa(s) --- Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"

# analisa a msg do predio [andar] sobre a pessoa
def resposta_predio(pessoa, msg):
    if msg[1] == 'ok':
        lista_atual.append(pessoa["id"]) # adiciona uma pessoa no condominio
        print "\n> Entrou um " + pessoa["id"] + " no condominio\n"
        print "Condominio : [" + str(len(lista_atual)) + "] pessoa(s) --- Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"

        # caso na resposta venha pessoa(s) para serem removidas do predio
        if msg[2] != "vazio": # existem pessoas que foram removidas, entao remova-as do predio
            funcao_remove(msg[2])
        
        # informacoes sobre o condominio [gerenciador] enviadas para o cliente
        dic = {1 : len(lista_atual), 2 : len(lista_espera)}
        s.send(str(dic))
    # elif msg[1] == "erro":
    #     print "O " + pessoa["id"] + " nao possui acesso ao predio interessado!\n"
    elif msg[1] == "listacheia":
        if len(lista_espera) < lista_espera_MAX:
            lista_espera.append(pessoa)
            print "Condominio : [" + str(len(lista_atual)) + "] pessoa(s) --- 2 Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
        else:
            print "\n O condominio esta cheio no momento, volte mais tarde!\n"
    # elif msg[1] == "removido": ### 
    #     lista_atual.pop(0)
    # caso na resposta venha pessoa(s) para serem removidas do predio
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


controle = 1
while controle != 0:

    

    # manda a pessoa recebida do cliente para o predio correto
    pessoa = ast.literal_eval(s.recv())

    if len(lista_atual) < condominio_MAX:

        # verifica se nao existe pessoas na lista de espera do condominio
        # while len(lista_espera) > 0 and len(lista_atual) < condominio_MAX: ### talvez inutil
        #     verifica_pessoas_fila_espera()

        # envia a pessoa para o predio 1
        if pessoa["predio"] == "predio1":
            s2.send(str(pessoa))
            msg = ast.literal_eval(s2.recv())
            # print msg

        resposta_predio(pessoa, msg)
    elif len(lista_espera) < lista_espera_MAX:
        lista_espera.append(pessoa)
        print "Condominio : [" + str(len(lista_atual)) + "] pessoa(s) --- 4 Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
    elif len(lista_espera) >= lista_espera_MAX:
        print "\n*** Fila do condominio esta cheia ***\n"
        # pass