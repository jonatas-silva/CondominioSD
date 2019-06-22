# bibliotecas utilizadas

import zmq
import ast # biblioteca usada para converter String em um Dicionario
from random import * # randint(0,9) , random.choice('abc') # Gera numeros aleatorios inteiros
import time
# temporizador = 0 # [0] desabilitado, [1 ou mais] habilitado, quanto maior mais devagar

# REDE [ AWS - JONATAS OLIVEIRA ]

GERENCIADOR_PUBLICO = "34.227.72.58"
GERENCIADOR_PRIVADO = "172.31.43.246"
PREDIO_PUBLICO = "54.165.253.103"
PREDIO_PRIVADO = "172.31.39.90"
ANDAR_PRIVADO = "172.31.81.46"
ANDAR2_PRIVADO = "172.31.81.255"
ANDAR3_PRIVADO = "172.31.87.59"

# REDE [ AWS - DEMAIS INTEGRANTES DO GRUPO ]

# PREDIO2_PUBLICO = "0.0.0.0"
# PREDIO2_PRIVADO = "0.0.0.0"
# PREDIO3_PUBLICO = "0.0.0.0"
# PREDIO3_PRIVADO = "0.0.0.0"
# PREDIO3_PUBLICO = "0.0.0.0"
# PREDIO3_PRIVADO = "0.0.0.0"

# LEGENDA PORTAS [   cliente   ->   servidor  ]
PORT1 = "5555" # [ cliente_app -> gerenciador ]
PORT2 = "5556" # [ cliente_adm -> server_predio ] e [ gerenciador -> server_predio ] e [ gerenciador -> server_predio2 ] e [ gerenciador -> server_predio3 ] e [ gerenciador -> server_predio4 ]
PORT3 = "5557" # [ server_predio -> server_andar ]
PORT4 = "5558" # [ server_andar -> server_predio ] e [ server_andar2 -> server_predio ] e [ server_andar3 -> server_predio ]
PORT6 = "5560" # [ server_predio -> server_andar2 ]
PORT7 = "5561" # [ server_predio -> server_andar3 ]



# ENDERECOS NECESSARIOS APENAS PARA EXECUCAO EM MAQUINA LOCAL

# HOST  = "192.168.0.73" # ip privado local
# # HOST2  = "192.168.0.73" # ip publico AWS [Predio 2]
# # HOST3  = "192.168.0.73" # ip publico AWS [Predio 3]
# # HOST4  = "192.168.0.73" # ip publico AWS [Predio 4]
# HOST5  = "52.205.213.232" # ip publico AWS [Predio 1]

# PORTAS NECESSARIAS APENAS PARA EXECUCAO EM MAQUINA LOCAL

# PORT5 = "5559" # [ gerenciador -> server_predio2 ]
# PORT8 = "5562" # [ gerenciador -> server_predio3 ]
# PORT9 = "5563" # [ gerenciador -> server_predio4 ]