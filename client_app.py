from constCS import *

context = zmq.Context()
p = "tcp://"+ HOST +":"+ PORT1 # how and where to connect
s  = context.socket(zmq.REQ)    # cria socket de requisicao
s.connect(p)                   # block until connected

frequentadores = ["visitante", "funcionario do condominio", "funcionario de empresa"] # lista
frequentadores_dic = {1 : "visitante", 2 : "funcionario do condominio", 3 : "funcionario de empresa"} # dicionario
predios = {1 : "predio1", 2 : "predio2", 3 : "predio3", 4 : "predio4"}
andares = {1 : "andar1", 2 : "andar2", 3 : "andar3", 4 : "andar4"}

# controle de acesso
# def controle_acesso(id):
#     if id == "visitante":
#         acesso = [randint(1,4)]
#     elif id == "funcionario do condominio":
#         acesso = [1, 2, 3, 4]
#     else:
#         acesso = [randint(1,4), randint(1,4)]
#         while acesso[0] == acesso[1]:
#             acesso = [randint(1,4), randint(1,4)]
#     return acesso

controle, lista_atual_qnt, lista_espera_qnt = 1, 0, 0
while controle != 0:

    op = input ("\n** BEM VINDO AO SIMULADOR DE CONDOMINIO DE EMPRESAS **\n\n\t1 - Teste automatizado\n\t2 - Inserir uma pessoa manualmente\n\t3 - Total pessoas no Condominio\n\t4 - Total pessoas na lista de espera do Condominio\n\t0 - SAIR\n>: ")
    if op == 1: # teste automatizado
        casos_teste = input ("\nInforme a quantidade de instancias (aleatorias) de entrada\n>: ")
        for i in range(casos_teste):
            id = choice(frequentadores) # definindo (aleatoriamente) um tipo de pessoa
            # acesso = controle_acesso(id) # controle de acesso

            # exemplo de um tipo de Pessoa
            pessoa = {"id" : str(id), "predio" : "predio1", "andar" : "andar1", "acesso" : "###"}
            # print str(pessoa)

            s.send(str(pessoa)) # manda a pessoa para o gerenciador
            msg = ast.literal_eval(s.recv())
            print msg
            lista_atual_qnt = (msg[1] + msg[2])
            lista_espera_qnt = msg[2]

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
        
        s.send(str(pessoa)) # manda a pessoa para o gerenciador
        msg = ast.literal_eval(s.recv())
        lista_atual_qnt = (msg[1] + msg[2])
        lista_espera_qnt = msg[2]

    elif op == 3: # qnt de pessoas no condominio
        print "\nQnt de pessoas no Condominio: " + str(lista_atual_qnt)
        a = raw_input ("\nEnter para continuar...")
    
    elif op == 4: # qnt de pessoas na lista de espera do condominio
        print "\nQnt de pessoas na lista de espera do Condominio: " + str(lista_espera_qnt)
        a = raw_input ("\nEnter para continuar...")
    
    elif op == 0: # sair
        controle = 0
        
    else:
        print "\nComando invalido, tente novamente!\n"