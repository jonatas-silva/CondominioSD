from constCS import *

# CLIENTE DO PREDIO 1
context = zmq.Context()
# p = "tcp://"+ HOST +":"+ PORT2 # how and where to connect
p = "tcp://"+ PREDIO_PUBLICO +":"+ PORT2 # how and where to connect
s  = context.socket(zmq.REQ)    # cria socket de requisicao
s.connect(p)                   # block until connected

# # CLIENTE DO PREDIO 2
# context = zmq.Context()
# # p2 = "tcp://"+ HOST +":"+ PORT2 # how and where to connect
# p2 = "tcp://"+ HOST2 +":"+ PORT2 # how and where to connect
# s2  = context.socket(zmq.REQ)    # cria socket de requisicao
# s2.connect(p2)                   # block until connected

# # CLIENTE DO PREDIO 3
# context = zmq.Context()
# # p3 = "tcp://"+ HOST +":"+ PORT2 # how and where to connect
# p3 = "tcp://"+ HOST3 +":"+ PORT2 # how and where to connect
# s3  = context.socket(zmq.REQ)    # cria socket de requisicao
# s3.connect(p3)                   # block until connected

# # CLIENTE DO PREDIO 4
# context = zmq.Context()
# # p4 = "tcp://"+ HOST +":"+ PORT2 # how and where to connect
# p4 = "tcp://"+ HOST4 +":"+ PORT2 # how and where to connect
# s4  = context.socket(zmq.REQ)    # cria socket de requisicao
# s4.connect(p4)                   # block until connected

predios = {1 : "predio1", 2 : "predio2", 3 : "predio3", 4 : "predio4"}
predio_socket = {"predio1" : s} # , "predio2" : s2, "predio3" : s3, "predio4" : s4}

controle, lista_atual_qnt, lista_espera_qnt, capacidade_atual, tamanho_atual = 1, 0, 0, 45, 15
while controle != 0:

    op = input ("\n** BEM VINDO - MODULO ADMINISTRADOR **\n\n\t[1] - Alterar a capacidade maxima de um Predio\n\t[2] - Alterar o tamanho da lista de espera de um Predio\n\t[0] - SAIR\n>: ")
    if op == 1: # alterar capacidade maximo do predio 1
        predio_desejado = 0
        while predio_desejado not in [1, 2, 3, 4]:
            predio_desejado = input ("\nInforme qual o PREDIO desejado? [1 , 2 , 3, 4]\n>: ")
        
        nova_capacidade = input ("\nInforme a nova capacidade [ATUAL: {}]\n:> ".format(capacidade_atual))
        capacidade_atual = nova_capacidade
        dic = {1 : nova_capacidade}
        predio_socket[predios[predio_desejado]].send(str(dic))
        resposta = ast.literal_eval(predio_socket[predios[predio_desejado]].recv())
        if resposta[1] == "ok":
            print "\n************************************"
            # print "| Nova capacidade do predio1 = 10 |"
            print "| Nova capacidade do predio " + str(predio_desejado) + " = " + str(nova_capacidade) + " |"
            print "************************************\n"
            time.sleep(2)
        else:
            print "\nErro ao aplicar nova capacidade maxima do predio \n" + str(predio_desejado) + "!\n"
            time.sleep(2)

    elif op == 2:
        predio_desejado = 0
        while predio_desejado not in [1, 2, 3, 4]:
            predio_desejado = input ("\nInforme qual o PREDIO desejado? [1 , 2 , 3, 4]\n>: ")
                
        novo_tamanho = input ("\nInforme o novo tamanho da lista de espera [ATUAL: {}]\n:> ".format(tamanho_atual))
        tamanho_atual = novo_tamanho
        dic = {2 : novo_tamanho}
        predio_socket[predios[predio_desejado]].send(str(dic))
        resposta = ast.literal_eval(predio_socket[predios[predio_desejado]].recv())
        if resposta[1] == "ok":
            print "\n*******************************************************"
            # print "| Nova capacidade da lista de espera do predio 1 = 10 |"
            print "| Nova capacidade da lista de espera do predio " + str(predio_desejado) + " = " + str(novo_tamanho) + " |"
            print "*******************************************************\n"
            time.sleep(2)
        else:
            print "\nErro ao aplicar nova capacidade maxima da lista do predio \n" + str(predio_desejado) + "!\n"
            time.sleep(2)

    # elif op == 3:

    # elif op == 4:
    
    # elif op == 5:
    
    elif op == 0: # sair
        controle = 0
        
    else:
        print "\nComando invalido, tente novamente!\n"