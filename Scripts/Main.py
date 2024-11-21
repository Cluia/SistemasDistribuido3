import random
import threading
import time
import queue

class Atendente:
    def __init__(self, id, tipo):
        self.id = id
        self.tipo = tipo
        self.status = "livre"

class Servidor:
    def __init__(self, nome, capacidade_max):
        self.nome = nome
        self.capacidade_max = capacidade_max
        self.atendentes = []
        self.configurar_atendentes()

    def configurar_atendentes(self):
        num_tecnico = random.randint(1, self.capacidade_max // 2)
        num_vendas = self.capacidade_max - num_tecnico
        self.atendentes = [Atendente(f"tec_{i}_{self.nome}", "suporte_tecnico") for i in range(num_tecnico)]
        self.atendentes += [Atendente(f"ven_{i}_{self.nome}", "vendas") for i in range(num_vendas)]
        print(f"[DEBUG] {self.nome}: Criados {num_tecnico} atendentes de suporte técnico e {num_vendas} de vendas.")

    def obter_atendente_livre(self, tipo):
        for atendente in self.atendentes:
            if atendente.tipo == tipo and atendente.status == "livre":
                atendente.status = "ocupado"
                return atendente
        return None

class SistemaAtendimento:
    def __init__(self, servidores, capacidade_buffer=50):
        self.servidores = servidores
        self.fila_suporte = queue.Queue()
        self.fila_vendas = queue.Queue()
        self.capacidade_buffer = capacidade_buffer
        self.logs = []
        self.ultimo_servidor_usado = -1  # Para roun

    def gerar_solicitacoes(self):
        num_solicitacoes = random.randint(10, 20)
        for _ in range(num_solicitacoes):
            tipo = random.choice(["suporte_tecnico", "vendas"])
            if tipo == "suporte_tecnico":
                if self.fila_suporte.qsize() < self.capacidade_buffer:
                    self.fila_suporte.put("Problema técnico")
                else:
                    self.logs.append("Falha: Buffer de suporte técnico estourou")
                    return False
            else:
                if self.fila_vendas.qsize() < self.capacidade_buffer:
                    self.fila_vendas.put("Pedido de vendas")
                else:
                    self.logs.append("Falha: Buffer de vendas estourou")
                    return False
        return True

    def processar_solicitacoes(self):
        while not self.fila_suporte.empty():
            self.atribuir_solicitacao(self.fila_suporte.get(), "suporte_tecnico")
        while not self.fila_vendas.empty():
            self.atribuir_solicitacao(self.fila_vendas.get(), "vendas")

    def atribuir_solicitacao(self, solicitacao, tipo):
        num_servidores = len(self.servidores)
        for _ in range(num_servidores):  # Round-robin entre servidores
            self.ultimo_servidor_usado = (self.ultimo_servidor_usado + 1) % num_servidores
            servidor = self.servidores[self.ultimo_servidor_usado]
            atendente = servidor.obter_atendente_livre(tipo)
            if atendente:
                self.logs.append(f"Atendente {atendente.id} (Tipo: {atendente.tipo}) do {servidor.nome} atendendo a solicitação: {solicitacao}")
                time.sleep(random.uniform(0.1, 0.5))  # Simula tempo de atendimento
                atendente.status = "livre"
                return
        self.logs.append(f"Sem atendentes livres para {tipo}. Tentativa de redirecionamento falhou.")

class Supervisor:
    def __init__(self, sistema):
        self.sistema = sistema

    def monitorar_falhas(self):
        while True:
            for servidor in self.sistema.servidores:
                for atendente in servidor.atendentes:
                    if atendente.status == "ocupado":
                        falha_prob = random.random()
                        if falha_prob < 0.1:  # 10% de chance de falha
                            self.sistema.logs.append(f"Atendente {atendente.id} falhou!")
                            atendente.status = "livre"
                            self.redistribuir_solicitacao(atendente.tipo)
            time.sleep(1)

    def redistribuir_solicitacao(self, tipo):
        self.sistema.logs.append(f"Redistribuindo solicitações para o tipo: {tipo}")
        for servidor in self.sistema.servidores:
            atendente_novo = servidor.obter_atendente_livre(tipo)
            if atendente_novo:
                self.sistema.logs.append(f"Solicitação realocada para {atendente_novo.id} do servidor {servidor.nome}")
                break

def executar_simulacao(timesteps=100):
    # Configuração dos servidores
    servidor_a = Servidor("Servidor A", capacidade_max=5)
    servidor_b = Servidor("Servidor B", capacidade_max=7)
    servidor_c = Servidor("Servidor C", capacidade_max=10)
    servidores = [servidor_a, servidor_b, servidor_c]

    # Inicialização do sistema e supervisor
    sistema = SistemaAtendimento(servidores)
    supervisor = Supervisor(sistema)

    # Thread do supervisor para monitorar falhas
    threading.Thread(target=supervisor.monitorar_falhas, daemon=True).start()

    # Simulação por timesteps
    for t in range(timesteps):
        if not sistema.gerar_solicitacoes():
            sistema.logs.append(f"Execução terminada no timestep {t} por falha no buffer.")
            break
        sistema.processar_solicitacoes()
        time.sleep(0.1)  # Intervalo entre timesteps

    # Exibição dos logs no final
    for log in sistema.logs:
        print(log, flush=True)

# Executa a simulação
executar_simulacao(timesteps = 30)
