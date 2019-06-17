# CondominioSD
Repositório de um projeto de Complexo de Condomínios para a disciplina de Sistemas Distribuídos.

Neste trabalho utilizamos de Cliente-servidor para simular um sistema distribuído.
A fim rodar o programa, dividimos o código em 5 diferentes scripts. 
3 deles representando andar, prédio e campus(scripts executáveis).

- Campus sendo apenas um cliente que gera as instâncias de visitante, funcionário-campus e funcionário-prédio enviando-os a seus respectivos prédios utilizando de endereços externos no AWS fixos, chamados IPs elásticos, assim como processando-os quanto a disponibilidade de vagas no campus . representado pelo script client_app.py.
- O prédio sendo um cliente-servidor que recebe as instâncias e mensagens do campus, enviando as instâncias para seus respectivos andares e replicando quando necessário para o campus quanto a aceitação ou negação da entrada da instância. Representado pelo script server_predio.py.
- Andares são somente servidor que recebem e só replicam às mensagens enviadas dos prédios, tais mensagens representando a aceitação ou negação da instância.Representado pelo script server_andar.py.
	Em ambos o campus, prédio e andar temos funções que processam a disponibilidade, a fila de espera, adição e remoção de instâncias.
	Temos também os Scripts ConstCS.py e constCS2.py que precisam estar na mesma pasta dos outros scripts uma vez que estes constCS são importados, dando acesso aos endereços IPs contidos neles, sendo assim scripts não-executáveis.(atualmente testamos apenas com um número pequeno de andares e somente um prédio). O ConstCS contém os endereços do campus e dos prédios, o ConstCS2 o do andar e dos prédios. Host e Host2 na versão atual são, respectivamente o endereço/IP do campus/máquina e o prédio/máquina a qual o script se encontra, com o campus e prédio obviamente sendo máquinas diferentes. O Host de ConstCS2 é o endereço/IP do andar/máquina a qual o script servidor_andar se encontra. 
	Toda vez que trocar de máquinas deve-se configurar os IPs do ConstCS e ConstCS2.
 A ideia é colocar o ConstCS2 com o endereço respectivo de cada andar apenas, acessando o IP de seu respectivo prédio.
	ao executar cada script(em diferentes máquinas cada um dos 3 executáveis) começa-se pelo andar(máquina com server_andar.py), em seguida pelo prédio(máquina com server_prédio.py) e finalmente o campus(client_app.py) a partir deste momento o client_app irá perguntar caso queira fazer testes automatizados, com as instâncias sendo geradas automaticamente de forma aleatória, ou manualmente com o usuário controlando a permissão e perfil(visitante, funcionário-campus, funcionário-prédio) de cada instância. Finalmente será pedido o número de instâncias e dependendo da escolha anterior, as instâncias serão geradas uma por uma pelo usuário ou máquina.
	Enquanto isso, os servidores andar e prédio irão processar as instâncias, aceitá-las nos prédios e andares, criar filas(através de vetores, armazenando o perfil e suas credenciais), remover instâncias ou adicionar da fila de forma automática.
