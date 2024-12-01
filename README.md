# SistemasDistribuido3

Descrição:
Este programa simula um sistema de atendimento com múltiplos servidores, atendentes e filas de solicitações. Ele distribui tarefas entre atendentes com base em disponibilidade e tipo de serviço (suporte técnico ou vendas), monitora falhas, e registra logs de operações e transferências de solicitações.

Funcionalidades Principais:
Configuração automática de servidores e atendentes.
Processamento de filas de solicitações de suporte técnico e vendas.
Monitoramento contínuo de falhas nos atendimentos.
Redistribuição de solicitações em caso de falhas.
Registro detalhado de operações em logs.
Exibição de relatórios ao final da execução.
(Mudar de atendente caso haja falhas) - não consegui.

--------------------------------------------------------------------------------------

Dependências:
Python 3.6 ou superior

Bibliotecas nativas do Python:
random
threading
time
queue

----------------------------------------------------------------------------------------

Exemplo de Saída

Relatório Final:
Tabela de Status de Servidor:
Servidor       Atendimentos    Capacidade    Falhas
Servidor A     15             5             1
Servidor B     10             7             2
Servidor C     20             10            0

Tabela de Transferências de Atendimento:
Número total de transferências: 5
Falhas em transferências: 1

-------------------------------------------------------------------------------------


"3. Lições aprendidas e boas práticas: O que foi preciso mudar desde o projeto inicial até a versão final? Quais os maiores aprendizados na opinião do grupo."
Eu demorei muito para notar que não estava de fato realocando as solicitações com problemas, apenas mostrando um print que dizia estar trocando, por conta disso não consegui ir a fundo para descobrir o por que não consigo fazer funcionar. No começo achei que fazer um sistema com vários servidores e atendimentos seria beem desafiador, mas é bem mais simples do que esperava, mesmo não saindo perfeito.
