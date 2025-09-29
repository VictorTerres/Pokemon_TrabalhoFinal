"""PokémonSaldo.ipynb

O presente código, pretende implementar alguns algoritmos descobertos durante o semestre na aula de IA para resolução de um problema simples. O Problema consiste na resolução de um dilema de escolhas, temos um cenário ficticio com caracteristicas ficticias, e o objetivo é resolve-lo da melhor forma possivel.

Um treinador tem a sua disposição uma quantidade aleatória de Pokémon para montar seu time ideal, porém ele dispõe de muitos monstrinhos distintos. Para contextualização, cada pokémon tem entre um e dois tipos associados a si, nunca mais que dois, e cada um desses tipos tem vantagens e desvantagens contra outros tipos, o que gera os conflitos e estratégias de batalha. O nosso treinador em questão deseja montar um time de 6 monstrinhos (escolhendo entre os que estão a sua disposição) de uma maneira que cubra a maior quantidade de vantagens possíveis. Como são 18 tipos no total, quanto mais próximo a esse valor melhor.

Para resolver esse problema então, o programa irá primeiramente gerar n Pokémon aleatórios, e então montar um time aleatório. Foi implementada uma função que gera os Pokémon, bem como uma que calcula a quantidade de vantagens que um time cobre.

Para otimizarmos, foram implementados 3 algoritmos distintos de escolha de times, que focarão em garantir que o time formado esteja mais próximo de 18 vantagens no total.
"""
from collections import Counter
import random

# Classificação e listagem de cada um dos tipos e suas vantagens, desvantagens e imunidades. Pode se notar que cada tipo tem vantagens, desvantagens e imunidades únicas.
class Tipo:
    def __init__(self, nome, vantagens, desvantagens, imunidades):
     self.nome = nome
     self.vantagens = vantagens
     self.desvantagens = desvantagens
     self.imunidades = imunidades

    def __repr__(self):
      return self.nome

tipos = [
    Tipo('grama', ['agua', 'terra', 'pedra'], ['fogo', 'gelo', 'venenoso', 'voador', 'inseto'], []),
    Tipo('fogo', ['grama', 'gelo', 'inseto', 'metal'], ['agua', 'pedra', 'terra'], []),
    Tipo('agua', ['fogo', 'terra', 'pedra'], ['grama', 'eletrico'], []),
    Tipo('eletrico', ['agua', 'voador'], ['terra'], []),
    Tipo('voador', ['grama', 'lutador', 'inseto'], ['gelo', 'eletrico', 'pedra'], ['terra']),
    Tipo('terra', ['fogo', 'eletrico', 'venenoso', 'pedra', 'metal'], ['agua', 'gelo', 'grama'], ['eletrico']),
    Tipo('pedra', ['fogo', 'gelo', 'voador', 'inseto'], ['agua', 'lutador', 'grama', 'metal', 'terra'], []),
    Tipo('metal', ['gelo', 'pedra', 'fada'], ['lutador', 'fogo', 'terra'], ['venenoso']),
    Tipo('normal', [], ['lutador'], ['fantasma']),
    Tipo('lutador', ['normal', 'gelo', 'pedra', 'sombrio', 'metal'], ['voador', 'psiquico', 'fada'], []),
    Tipo('psiquico', ['lutador', 'venenoso'], ['sombrio', 'inseto', 'fantasma'], []),
    Tipo('fantasma', ['psiquico', 'fantasma'], ['sombrio', 'fantasma'], ['normal', 'lutador']),
    Tipo('sombrio', ['psiquico', 'fantasma'], ['fada', 'inseto', 'lutador'], ['psiquico']),
    Tipo('inseto', ['grama', 'psiquico', 'sombrio'], ['fogo', 'pedra', 'voador'], []),
    Tipo('gelo', ['grama', 'terra', 'voador', 'dragao'], ['fogo', 'pedra', 'lutador', 'metal'], []),
    Tipo('fada', ['lutador', 'dragao', 'sombrio'], ['metal', 'venenoso'], ['dragao']),
    Tipo('venenoso', ['grama', 'fada'], ['terra', 'psiquico'], []),
    Tipo('dragao', ['dragao'], ['dragao', 'gelo', 'fada'], []),
]

# Tipos proibidos de serem combinados
proibidos = {
    tuple(sorted(['normal', 'gelo'])),
    tuple(sorted(['normal', 'inseto'])),
    tuple(sorted(['normal', 'pedra'])),
    tuple(sorted(['normal', 'metal'])),
    tuple(sorted(['fogo', 'fada'])),
    tuple(sorted(['gelo', 'venenoso'])),
    tuple(sorted(['terra', 'fada'])),
    tuple(sorted(['inseto', 'dragao'])),
    tuple(sorted(['pedra', 'fantasma'])),
    tuple(sorted(['normal', 'fantasma'])),
    tuple(sorted(['fogo', 'agua'])),
    tuple(sorted(['fogo', 'eletrico'])),
    tuple(sorted(['fogo', 'gelo'])),
    tuple(sorted(['eletrico', 'grama'])),
    tuple(sorted(['eletrico', 'psiquico'])),
    tuple(sorted(['gelo', 'metal'])),
    tuple(sorted(['gelo', 'fada'])),
    tuple(sorted(['psiquico', 'fantasma'])),
    tuple(sorted(['dragao', 'fada']))
}


# Parâmetros Gerais dos Algoritmos
taxa_mutacao = 0.1
tamanho_populacao = 100
geracoes = 100

# Função que gera Pokémon aleatórios, combinando tipos em pares.
def gera_pokemon(tipos):
    """Gera um Pokémon válido, evitando combinações proibidas"""
    while True:
        p = random.choices(tipos, k=2)
        par = tuple(sorted([p[0].nome, p[1].nome]))
        if par not in proibidos:
            return p

pokemon = [gera_pokemon(tipos) for _ in range(tamanho_populacao)]
for p in pokemon:
    print(p)

# Escolha de Pokémon Aleatórios sem repetição
time = random.sample(pokemon, k=6)

# Funções que listam as vantagens, desvantagens e imunidades do time
def lista_vantagens(time):
    """Retorna (lista_de_vantagens_unicas, total) — vantagens contadas como únicas."""
    vantagens_unicas = set()
    for p in time:
        vantagens_unicas.update(p[0].vantagens)
        vantagens_unicas.update(p[1].vantagens)
    vantagens = list(vantagens_unicas)
    total_vantagens = len(vantagens)
    return vantagens, total_vantagens

def lista_desvantagens(time):
    """Retorna (lista_de_desvantagens_unicas, total) — desvantagens contadas como únicas."""
    desvantagens_unicas = set()
    for p in time:
        desvantagens_unicas.update(p[0].desvantagens)
        desvantagens_unicas.update(p[1].desvantagens)
    desvantagens = list(desvantagens_unicas)
    total_desvantagens = len(desvantagens)
    return desvantagens, total_desvantagens

def lista_imunidades(time):
    """Retorna (lista_de_imunidades_unicas, total) — imunidades contadas como únicas."""
    imunidades_unicas = set()
    for p in time:
        imunidades_unicas.update(p[0].imunidades)
        imunidades_unicas.update(p[1].imunidades)
    imunidades = list(imunidades_unicas)
    total_imunidades = len(imunidades)
    return imunidades, total_imunidades

# Pesos globais ajustáveis
PESO_VANTAGEM = 1.0      # quanto maior, mais foco em vantagens
PESO_DESVANTAGEM = 0.5    # quanto maior, mais penaliza fraquezas
PESO_IMUNIDADE = 0.2      # quanto maior, mais valor às imunidades
PENALIDADE_DUPLICACAO = 1.5  # penalidade por repetição de cobertura

def saldo(time, peso_vantagem=PESO_VANTAGEM, peso_desvantagem=PESO_DESVANTAGEM,
          peso_imunidade=PESO_IMUNIDADE, penalidade_duplicacao=PENALIDADE_DUPLICACAO,
          penalizar_por='tipo'):
    """
    Calcula o saldo do time considerando pesos para vantagens, desvantagens e imunidades.
    
    penalizar_por: 'coverage' -> penaliza duplicação de vantagens/imunidades
                    'tipo'     -> penaliza repetição de tipos nos pokémon do time
    """
    vant_counter = Counter()
    imun_counter = Counter()
    des_set = set()
    tipo_counter = Counter()  # conta a repetição de tipos do time

    for p in time:
        # Coverage
        vant_counter.update(p[0].vantagens)
        vant_counter.update(p[1].vantagens)
        imun_counter.update(p[0].imunidades)
        imun_counter.update(p[1].imunidades)
        des_set.update(p[0].desvantagens)
        des_set.update(p[1].desvantagens)

        # Tipos do Pokémon
        tipo_counter.update([p[0].nome, p[1].nome])

    total_vant_unicas = len(set(vant_counter.keys()))
    total_des_unicas = len(des_set)
    total_imun_unicas = len(set(imun_counter.keys()))

    # Penalidade
    if penalizar_por == 'coverage':
        duplicacoes_vant = sum(max(0, c - 1) for c in vant_counter.values())
        duplicacoes_imun = sum(max(0, c - 1) for c in imun_counter.values())
        penalidade_total = penalidade_duplicacao * (duplicacoes_vant + duplicacoes_imun)
    elif penalizar_por == 'tipo':
        duplicacoes_tipo = sum(max(0, c - 1) for c in tipo_counter.values())
        penalidade_total = penalidade_duplicacao * duplicacoes_tipo
    else:
        penalidade_total = 0

    score = (peso_vantagem * total_vant_unicas
             - peso_desvantagem * total_des_unicas
             + peso_imunidade * total_imun_unicas
             - penalidade_total)
    return score

# Gerar time inicial aleatório
print(f'\nTime Inicial Gerado Aleatoriamente: {time} com {lista_vantagens(time)[1]} vantagens e {lista_desvantagens(time)[1]} desvantagens e {lista_imunidades(time)[1]} imunidades e saldo {saldo(time)}')

# Função que muda o time aleatoriamente
def aleatoriza(time):
    pkm_antigo = random.choice(time)
    pkm_novo = random.choice(pokemon)
    time_novo = list(time)
    time_novo[time_novo.index(pkm_antigo)] = pkm_novo
    _, total_vantagens = lista_vantagens(time_novo)
    _, total_desvantagens = lista_desvantagens(time_novo)
    _, total_imunidades = lista_imunidades(time)
    total_saldo = saldo(time_novo)
    return time_novo

# Função que tenta melhorar o time utilizando Algoritmo Greedy
def greedy(time):
    _, total_vantagens = lista_vantagens(time)
    _, total_desvantagens = lista_desvantagens(time)
    _, total_imunidades = lista_imunidades(time)
    saldo_inicial = saldo(time)
    pkm_antigo = random.choice(time)
    pkm_novo = random.choice(pokemon)
    time_novo = list(time)
    time_novo[time_novo.index(pkm_antigo)] = pkm_novo
    _, total_vantagens_novo = lista_vantagens(time_novo)
    _, total_desvantagens_novo = lista_desvantagens(time_novo)
    _, total_imunidades_novo = lista_imunidades(time_novo)
    saldo_novo = saldo(time_novo)
    if saldo_novo > saldo_inicial:
        return time_novo
    else:
        return time

# Função que tenta melhorar o time utilizando Algoritmo Hill Climbing
def hill_climbing(time, max_iter=10):
    _, total_vantagens = lista_vantagens(time)
    _, total_desvantagens = lista_desvantagens(time)
    _, total_imunidades = lista_imunidades(time)
    saldo_inicial = saldo(time)
    time_atual = time
    saldo_atual = saldo_inicial
    i = 0
    while i < max_iter:
        vizinhos = []
        for i in range(len(time)):
            for j in range(2):
                novo_pokemon = random.choice(pokemon)
                time_vizinho = list(time_atual)
                time_vizinho[i] = novo_pokemon
                saldo_vizinho = saldo(time_vizinho)
                vizinhos.append((time_vizinho, saldo_vizinho))
        vizinhos = sorted(vizinhos, key=lambda x: x[1], reverse=True)
        if vizinhos[0][1] > saldo_atual:
            time_atual = vizinhos[0][0]
            saldo_atual = vizinhos[0][1]
        else:
            return time_atual
        i += 1
    return time_atual

# Conjunto de Funções que tenta melhorar o time utilizando Algoritmo Genético

# Função de Avaliação de Aptidão (Fitness)
def fitness(time):
    return saldo(time)

# Função de Seleção dos Pais por Torneio
def seleciona_pais(populacao):
    pai1 = random.choice(populacao)
    pai2 = random.choice(populacao)
    i = 0
    while pai2 == pai1 and i < 100:
        pai2 = random.choice(populacao)
        i = i+1
    if fitness(pai1) > fitness(pai2):
        return pai1
    else:
        return pai2

# Função de Crossover (Recombinação)
def crossover(pai1, pai2):
    filho = []
    for i in range(len(pai1)):
        gene_pai1 = pai1[i]
        gene_pai2 = pai2[i]
        if random.random() < 0.5:
            filho.append(gene_pai1)
        else:
            filho.append(gene_pai2)
    return filho

# Função de Mutação
def mutacao(filho):
    for i in range(len(filho)):
        if random.random() < taxa_mutacao:
            filho[i] = random.choice(pokemon)
    return filho

# Inicialização da População Aleatória
populacao = [random.sample(pokemon, k=6) for _ in range(tamanho_populacao)]

"""Comparação do desempenho de cada um dos times"""

time_1 = time

for i in range(geracoes):
    time_1 = aleatoriza(time_1)
    #print(f'Time após iteração {i+1}: {time_1} com saldo {saldo(time_1)}')
print(f'\nTime Final Gerado Aleatoriamente: {time_1} com vantagens, desvantagens, imunidades e saldo final: {lista_vantagens(time_1)[1]}, {lista_desvantagens(time_1)[1]}, {lista_imunidades(time_1)[1]}, {saldo(time_1)}')

time_2 = time

for i in range(geracoes):
    time_2 = greedy(time_2)
    #print(f'Time após iteração {i+1}: {time_2} com saldo {saldo(time_2)}')
print(f'\nTime Final Gerado Pelo Greedy: {time_2} com vantagens, desvantagens, imunidades e saldo final: {lista_vantagens(time_2)[1]}, {lista_desvantagens(time_2)[1]}, {lista_imunidades(time_2)[1]}, {saldo(time_2)}')

time_3 = time

for i in range(geracoes):
    time_3 = hill_climbing(time_3)
    #print(f'Time após iteração {i+1}: {time_3} com saldo {saldo(time_3)}')
print(f'\nTime Final Gerado Pelo Hill Climb: {time_3} com vantagens, desvantagens, imunidades e saldo final: {lista_vantagens(time_3)[1]}, {lista_desvantagens(time_3)[1]}, {lista_imunidades(time_3)[1]}, {saldo(time_3)}')

time_4 = time

for geracao in range(geracoes):
    #print(f'\nGeração {geracao+1}:')
    nova_populacao = []
    for i in range(tamanho_populacao):
        pai1 = seleciona_pais(populacao)
        pai2 = seleciona_pais(populacao)
        filho = crossover(pai1, pai2)
        filho = mutacao(filho)
        nova_populacao.append(filho)
        #print(f'Filho {i+1}: {filho}, Fitness: {fitness(filho)}')
    populacao = nova_populacao

time_4 = max(populacao, key=fitness)

print(f'\nTime Final Gerado Pelo Genético: {time_4} com {lista_vantagens(time_4)[1]} vantagens, {lista_desvantagens(time_4)[1]} desvantagens, {lista_imunidades(time_4)[1]} imunidades e saldo {saldo(time_4)}')


# Lista com todos os candidatos
times = [
    ("Aleatório", time_1),
    ("Greedy", time_2),
    ("Hill Climbing", time_3),
    ("Genético", time_4)
]

# Melhor time entre todos
melhor_nome, melhor_time = max(times, key=lambda x: fitness(x[1]))

print(f'\nMelhor time, {melhor_nome}: {melhor_time} '
      f'com {lista_vantagens(melhor_time)[1]} vantagens, '
      f'{lista_desvantagens(melhor_time)[1]} desvantagens, '
      f'{lista_imunidades(melhor_time)[1]} imunidades '
      f'e saldo {saldo(melhor_time)}')