from constCS import *

# SERVIDOR DO GERENCIADOR
context = zmq.Context()
p = "tcp://"+ HOST +":"+ PORT2 # how and where to connect
s  = context.socket(zmq.REP)    # servidor do gerenciador
s.bind(p)                      # bind socket to address

# CLIENTE DO ANDAR
pa1 = "tcp://"+ HOST +":"+ PORT3 # ip e porta do andar 1
ca1 = context.socket(zmq.REQ)     # cliente do Andar 1
ca1.connect(pa1)                   # conectado no Andar 1

# SERVIDOR DO ANDAR
p3 = "tcp://"+ HOST +":"+ PORT4 # how and where to connect
s3  = context.socket(zmq.REP)    # servidor do Andar
s3.bind(p3)                      # bind socket to address

# CLIENTE DO GERENCIADOR
p4 = "tcp://"+ HOST +":"+ PORT5 # how and where to connect
s4 = context.socket(zmq.REQ)     # cliente do gerenciador
s4.connect(p4)                   # block until connected

predio_MAX = 15 # 45
lista_espera_MAX = 5 # 15
predio_atual = "predio1"
identificador_predio = {1 : "predio 1", 2 : "Predio 1"} # identificadores do predio
frequentadores = ["visitante", "funcionario do condominio", "funcionario de empresa"] # lista de ids
pessoasrem = "0 0 0"

# lista de pesoas na espera
lista_atual = [] # lista de pessoas que estao no andar
lista_espera = [] # lista de pessoas na espera

# remove a(s) pessoa(s) do predio que o andar ja removeu
def funcao_remove(msg2):
  msg2 = msg2.split()
  # 0 = visitante, 1 = func cond, 2 = func empresa
  for i in range(3):
    if int(msg2[i]) > 0:
      for j in range(int(msg2[i])):
        if len(lista_atual) > 0:
          res = lista_atual.remove(frequentadores[i])
          print "\n- Saiu um " + frequentadores[i] + " do " + identificador_predio[1] + "\n"
          time.sleep(1)
          print identificador_predio[2] + " : [" + str(len(lista_atual)) + "] pessoa(s) --- Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"

# verificar se nao existe pessoas na lista de espera do andar
def verifica_pessoas_fila_espera():
  # if len(lista_atual) < predio_MAX:
  pessoa = lista_espera.pop(0) # remove o primeiro da lista_espera e ...
  # print "espera = " + str(pessoa)
  funcao_verifica_predio_adiciona_pessoa(pessoa, "adiciona_sem" ,"sem")

def funcao_verifica_predio_adiciona_pessoa(pessoa, tipo, resposta):
  # verificando se a pessoa queria vir realmente para este predio
  if pessoa["predio"] == predio_atual:

    # mandar a pessoa para o ANDAR 1
    if pessoa["andar"] == "andar1":
      dic = {1 : "existe vaga?", "resposta" : str(resposta)}
      ca1.send(str(dic))
      temp = ast.literal_eval(ca1.recv()) # recebe resposta se existe vaga e [lista de pessoas removidas]
      # print temp
      if temp[1] == "existe_vaga": # caso andar 1 ainda tenha vaga
        
        dic = {1 : str(tipo)}
        dic[2] = pessoa
        ca1.send(str(dic)) # envia dicionario com pessoa
        msg = ast.literal_eval(ca1.recv()) # recebe resposta do andar {1 : status, 2 : qnt}
        
        if msg[1] == "ok": # pessoa entrou no andar
          lista_atual.append(pessoa["id"]) # adiciona uma pessoa no predio
          print "\n> Entrou um " + pessoa["id"] + " no " + identificador_predio[1] + "\n"
          print identificador_predio[2] + " : [" + str(len(lista_atual)) + "] pessoa(s) --- 2 Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
          
          # caso na resposta venha pessoa(s) para serem removidas do predio
          if msg[2] != "vazio": # existem pessoas que foram removidas, entao remova-as do predio
            funcao_remove(msg[2])

          if resposta == "com": # apenas responde se houver pedido de resposta
            s.send(str(msg)) # retorna um dic com [1] "ok"  e [2] qnt de pessoas a remover para o condominio, caso consiga adicionar a pessoa no predio e andar
        else:
          print "pessoa nao conseguiu entrar no andar\n" # nao pode acontecer
      
      elif temp[1] == "nao_existe_vaga":
        if len(lista_espera) < lista_espera_MAX: # caso ainda tenha vaga na lista de espera, adiciona a pessoa nela
          lista_espera.append(pessoa)
          print identificador_predio[2] + " : [" + str(len(lista_atual)) + "] pessoa(s) --- 3 Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
          dic = {1 : "ok"} # msg que identifica que pessoa foi adicionada na lista de espera com sucesso
          del(temp[1])
          dic.update(temp)
          # print str(dic) + " test"

          # caso na resposta venha pessoa(s) para serem removidas do predio
          if temp[2] != "vazio": # existem pessoas que foram removidas, entao remova-as do predio
            funcao_remove(temp[2])
            pessoas_list = pessoasrem.split() # salva as pessoas a remover para enviar ao gerenciador na proxima oportunidades
            mensagem_list = temp[2].split()
            soma = ""
            for i in range(3):
                soma += "" + str(int(pessoas_list[i]) + int(mensagem_list[i])) + " "
            pessoasrem = soma
            print pessoasrem

          if resposta == "sem":
            if pessoasrem != "0 0 0":
              pessoas_list = pessoasrem.split()
              mensagem_list = temp[2].split()
              soma = ""
              for i in range(3):
                  soma += "" + str(int(pessoas_list[i]) + int(mensagem_list[i])) + " "
              print soma
              del(temp[2])
              temp[2] = soma
              dic.update(temp)

          if resposta == "com": # apenas responde se houver pedido de resposta
            s.send(str(dic)) # retorna um dic com [1] "ok"  e [2] qnt de pessoas a remover para o condominio, caso consiga adicionar a pessoa no predio e andar
        elif len(lista_espera) >= lista_espera_MAX:
          print "\n*** Lista de espera do " + identificador_predio[1] + " esta cheia ***\n"
          dic = {1 : "listacheia"}
          s.send(str(dic))
  else:
      print "nao sou o predio correto\n" # nunca deve ocorrer
      s.send("erro")

while True:

  # dorme 1 segundo antes de continuar
  time.sleep(1)

  # se houver pessoa(s) na lista de espera e o Andar estiver vaga entao envia a pessoa
  if len(lista_espera) > 0:
    dic = {1 : "existe vaga?", "resposta" : "sem"}
    ca1.send(str(dic))
    resp = ast.literal_eval(ca1.recv())
    if resp[1] == "existe_vaga":
      verifica_pessoas_fila_espera()
  
  # recebe uma nova pessoa do condominio
  pessoa = ast.literal_eval(s.recv())    # converte uma string em dicionario
  # print "\nMsg recebida: " + pessoa["id"]

  if len(lista_atual) < predio_MAX:  # caso ainda tenha vaga no andar e o tamanho da lista de espera seja menor que lista_espera_MAX
    funcao_verifica_predio_adiciona_pessoa(pessoa, "adiciona", "com")
  elif len(lista_espera) < lista_espera_MAX: # caso ainda tenha vaga na lista de espera, adiciona a pessoa nela
    lista_espera.append(pessoa)
    print identificador_predio[2] + " : [" + str(len(lista_atual)) + "] pessoa(s) --- 4 Lista de espera : [" + str(len(lista_espera)) + "] pessoa(s)"
    dic = {1 : "ok"}
    s.send(str(dic)) # retorna "ok" para o condominio, caso consiga adicionar a pessoa no predio
  elif len(lista_espera) >= lista_espera_MAX:
    print "\n*** Lista de espera do " + identificador_predio[1] + " esta cheia ***\n"
    dic = {1 : "listacheia"}
    s.send(str(dic))
    if len(lista_atual) > 0:
      # funcao_remove()   # chama a funcao remove
      pass
    continue

    




