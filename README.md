Repositório de um projeto de Condomínios de edifícios comerciais para a disciplina de Sistemas Distribuídos.

Alunos: 
Guilherme Sampaio Sapiencia,
Jônatas da Silva Oliveira
Rodrigo Nakamuta Izawa
Romário Fernando Castro Azevedo Magalhães

Neste trabalho utilizamos arquitetura Cliente-servidor para simular um sistema distribuído. A fim rodar o programa, dividimos o código em 6 diferentes scripts executáveis. 3 deles representam, condomínio (gerenciador.py), prédio (server_predio.py) e andar (server_andar.py). 
Temos também o script constCS.py que precisa estar na mesma pasta dos outros scripts uma vez que este script não executável é importado dentro dos outros scripts executáveis, pois, contém as bibliotecas, endereços IPs e portas, todos necessários para os outros scripts executáveis.

Linguagem: Python 2.7

OBS¹: Os IP’s publicos do gerenciador (GERENCIADOR_PUBLICO) e de todos os prédios (PREDIO_PUBLICO, PREDIO2_PUBLICO) e etc, precisam ser alterados antes da execução do programa! [somente se os servidores ainda não estiverem rodando na AWS, pois caso esteja o arquivo já estará atualizado com o IP público dos servidores no arquivo constCS.py	

 Cliente (client_app.py) : é o script cliente que gera as instâncias de pessoas dos tipos: visitante, funcionário do condomínio e funcionário de empresa. Enviando-os ao gerenciador.py que por sua vez envia-os à seus respectivos prédios utilizando de endereços públicos ou privados na AWS, assim como processando-os quanto a disponibilidade de vagas no condomínio.

 Cliente Administrativo (client_adm.py) : script responsável por alterar a capacidade de pessoas e/ou tamanho fila de espera dos prédios.

 Gerenciador (gerenciador.py) : é o script cliente-servidor que atua como o condomínio. Responsável por receber as instâncias de pessoas do Cliente e repassar para o Prédio correto ao qual a pessoa se destina. Ao receber a resposta do Prédio o mesmo envia uma msg para o Cliente com a quantidade atual de pessoas no condomínio e quantidade atual de pessoas na lista de espera do condomínio. Caso não exista vaga no Prédio, esta pessoa é adicionada na fila de espera do gerenciador (condomínio).

 Prédio (server_predio.py) : é responsável por receber as instâncias de pessoas do gerenciador.py e/ou mensagens de configurações do client_adm.py, enviando as instâncias de pessoas para seus respectivos andares de destino ou aplicando as configurações das mensagens recebidas no prédio. Antes de enviar uma pessoa para um andar, o prédio verifica no andar em questão se existe vaga e apenas envia a pessoa caso exista a vaga, depois responde para o condomínio (gerenciador) quanto a aceitação ou negação da entrada da instância no destino. Caso não exista vaga no andar de destino, esta pessoa é adicionada na fila de espera do Prédio.

 Andares (server_andar.py) : é somente servidor que recebe as mensagens ou pessoas do prédio, tais mensagens são perguntas se existem ou não vaga no andar, responde com outra mensagem com a reposta, caso responda que existe vaga então a pessoa será recebida logo em seguida e adicionada no andar e uma mensagem “ok” será devolvida. Também existe uma função que elimina de tempos em tempos algumas pessoas do andar (aleatoriamente) e ao responder uma msg para o prédio encaminha as pessoas removidas propagando até o gerenciador (condomínio).

 No condomínio e prédio, temos uma fila atual (guarda a quantidade de pessoas atualmente dentro do estabelecimento) e fila de espera (guarda quantidade de pessoas na fila de espera do estabelecimento). 

OBS²: O controle de acesso não foi implementado neste trabalho.
