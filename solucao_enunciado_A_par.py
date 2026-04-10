# Checkpoint 1 - Enunciado A
# Simulacao de um centro de distribuicao com fila de pedidos
# Estruturas usadas: lista, tupla, dicionario, deque, DataFrame
# Tambem usei: ordenacao, recursao e graficos

import sys
sys.stdout.reconfigure(encoding="utf-8")  # fix para nao dar erro de acento no windows

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # coloquei isso pq sem ele o grafico trava o programa
import matplotlib.pyplot as plt
from collections import deque

# -----------------------------------------------------------
# Lendo os dados do arquivo CSV
# -----------------------------------------------------------

# carrego o csv num dataframe do pandas
df = pd.read_csv(r"C:\Users\mateu\Downloads\Check_point_1_dados_logistica_RA_final_par.csv")

print("=== DADOS DO ARQUIVO ===")
print(df)
print()

# -----------------------------------------------------------
# Criando uma lista de TUPLAS com os pedidos
# Usei tupla porque os dados de cada pedido nao devem ser alterados
# Cada tupla tem: (id, produto, urgencia, valor_total, modal, destino, horas)
# -----------------------------------------------------------

lista_pedidos = []  # lista que vai guardar as tuplas

for i, row in df.iterrows():
    # calculo o valor total do pedido
    valor_total = row["quantidade"] * row["valor_unitario"]

    # crio a tupla do pedido e adiciono na lista
    pedido = (
        row["pedido_id"],
        row["produto"],
        row["urgencia"],
        valor_total,
        row["modal"],
        row["cidade_destino"],
        row["tempo_estimado_horas"]
    )
    lista_pedidos.append(pedido)

print("=== PEDIDOS EM FORMATO DE TUPLA ===")
print("(id, produto, urgencia, valor_total, modal, destino, horas)")
for p in lista_pedidos:
    print(p)
print()

# -----------------------------------------------------------
# DICIONARIOS
# Um dicionario pra mapear urgencia -> numero (pra ordenar)
# Outro dicionario pra agrupar os pedidos por urgencia
# -----------------------------------------------------------

# quanto menor o numero, mais urgente e o pedido
prioridade_urgencia = {
    "alta": 1,
    "media": 2,
    "baixa": 3
}

# cores pra usar nos graficos depois
cores_urgencia = {
    "alta": "red",
    "media": "orange",
    "baixa": "green"
}

# aqui agrupa os pedidos por nivel de urgencia
pedidos_por_urgencia = {
    "alta": [],
    "media": [],
    "baixa": []
}

for pedido in lista_pedidos:
    nivel = pedido[2]  # urgencia esta na posicao 2 da tupla
    pedidos_por_urgencia[nivel].append(pedido)

print("=== PEDIDOS AGRUPADOS POR URGENCIA ===")
for nivel in pedidos_por_urgencia:
    nomes = []
    for p in pedidos_por_urgencia[nivel]:
        nomes.append(p[1])
    print(nivel.upper() + ": " + str(nomes))
print()

# -----------------------------------------------------------
# Ordenacao dos pedidos
# Ordeno primeiro por urgencia (alta=1 vem antes), depois por valor (maior primeiro)
# O sorted usa Timsort -> complexidade O(n log n)
# -----------------------------------------------------------

# uso uma funcao separada em vez de lambda pra ficar mais facil de entender
def criterio_ordenacao(pedido):
    urgencia = prioridade_urgencia[pedido[2]]
    valor = -pedido[3]  # negativo pra ordenar do maior pro menor
    return (urgencia, valor)

lista_ordenada = sorted(lista_pedidos, key=criterio_ordenacao)

print("=== PEDIDOS ORDENADOS POR URGENCIA E VALOR ===")
for p in lista_ordenada:
    print("ID:", p[0], "| Produto:", p[1], "| Urgencia:", p[2], "| Valor: R$", p[3], "| Modal:", p[4])
print()

# -----------------------------------------------------------
# DEQUE - Fila de expedicao do centro de distribuicao
# Uso deque porque ele permite adicionar no fim e remover do inicio de forma eficiente
# append() -> O(1)  |  popleft() -> O(1)
# -----------------------------------------------------------

fila_expedicao = deque()

print("=== ADICIONANDO PEDIDOS NA FILA ===")
for pedido in lista_ordenada:
    fila_expedicao.append(pedido)
    print("Pedido #" + str(pedido[0]) + " (" + pedido[1] + ") entrou na fila - urgencia: " + pedido[2])

print()
print("Total de pedidos na fila:", len(fila_expedicao))
print()

# -----------------------------------------------------------
# Processando a fila: retira um pedido por vez do inicio
# -----------------------------------------------------------

print("=== PROCESSANDO A FILA DE EXPEDICAO ===")
print("-" * 50)

ordem = 1
log_processamento = []  # lista de dicionarios com o historico

while len(fila_expedicao) > 0:
    pedido = fila_expedicao.popleft()  # remove o primeiro da fila

    print("Ordem:", ordem, "| #" + str(pedido[0]), pedido[1], "->", pedido[5], "| Modal:", pedido[4], "| Tempo:", pedido[6], "h")

    # salvo o registro do pedido como dicionario no historico
    registro = {
        "ordem": ordem,
        "pedido_id": pedido[0],
        "produto": pedido[1],
        "urgencia": pedido[2],
        "valor": pedido[3],
        "modal": pedido[4],
        "destino": pedido[5],
        "tempo_horas": pedido[6]
    }
    log_processamento.append(registro)
    ordem = ordem + 1

print()

# converto o log em DataFrame pra visualizar melhor
df_log = pd.DataFrame(log_processamento)
print("=== LOG DE EXPEDICAO (DataFrame) ===")
print(df_log)
print()

# -----------------------------------------------------------
# RECURSAO - calcula o valor total de todos os pedidos
# Caso base: quando o indice passa do tamanho da lista, retorna 0
# Caso recursivo: soma o valor do pedido atual + chama a funcao pro proximo
# Complexidade: O(n) porque passa por cada elemento uma vez
# -----------------------------------------------------------

def calcular_valor_total(lista, indice=0):
    # caso base: chegou no final da lista
    if indice == len(lista):
        return 0

    # caso recursivo: valor do pedido atual + total dos proximos
    return lista[indice]["valor"] + calcular_valor_total(lista, indice + 1)

total = calcular_valor_total(log_processamento)
print("Valor total expedido (calculado com recursao): R$", total)
print()

# -----------------------------------------------------------
# GRAFICOS
# Fiz um grafico pra cada analise e salvei em arquivos separados
# -----------------------------------------------------------

# Grafico 1: quantidade de pedidos por urgencia
plt.figure(figsize=(7, 5))

niveis = ["alta", "media", "baixa"]
quantidades = [
    len(pedidos_por_urgencia["alta"]),
    len(pedidos_por_urgencia["media"]),
    len(pedidos_por_urgencia["baixa"])
]
cores = [cores_urgencia["alta"], cores_urgencia["media"], cores_urgencia["baixa"]]

plt.bar(niveis, quantidades, color=cores, edgecolor="black")
plt.title("Quantidade de Pedidos por Urgencia")
plt.xlabel("Urgencia")
plt.ylabel("Quantidade")

# coloco o numero em cima de cada barra
for i in range(len(niveis)):
    plt.text(i, quantidades[i] + 0.05, str(quantidades[i]), ha="center")

plt.savefig(r"C:\Users\mateu\Downloads\CP1_Dynamic_Programming\grafico1_urgencia.png")
plt.close()
print("Grafico 1 salvo: grafico1_urgencia.png")

# Grafico 2: valor total por modal de transporte
plt.figure(figsize=(7, 5))

df["valor_total"] = df["quantidade"] * df["valor_unitario"]
valor_por_modal = df.groupby("modal")["valor_total"].sum()

plt.bar(valor_por_modal.index, valor_por_modal.values, color=["steelblue", "mediumpurple"], edgecolor="black")
plt.title("Valor Total por Modal de Transporte")
plt.xlabel("Modal")
plt.ylabel("Valor Total (R$)")

plt.savefig(r"C:\Users\mateu\Downloads\CP1_Dynamic_Programming\grafico2_modal.png")
plt.close()
print("Grafico 2 salvo: grafico2_modal.png")

# Grafico 3: tempo estimado de cada pedido na ordem de saida
plt.figure(figsize=(8, 5))

ordens = []
tempos = []
produtos = []
cores_barras = []

for registro in log_processamento:
    ordens.append(registro["ordem"])
    tempos.append(registro["tempo_horas"])
    produtos.append(registro["produto"])
    cores_barras.append(cores_urgencia[registro["urgencia"]])

plt.bar(ordens, tempos, color=cores_barras, edgecolor="black")
plt.title("Tempo Estimado por Ordem de Saida")
plt.xlabel("Pedido")
plt.ylabel("Tempo Estimado (horas)")
plt.xticks(ordens, produtos, rotation=20)
plt.tight_layout()

plt.savefig(r"C:\Users\mateu\Downloads\CP1_Dynamic_Programming\grafico3_tempo.png")
plt.close()
print("Grafico 3 salvo: grafico3_tempo.png")

# Grafico 4: pizza com status de pagamento
plt.figure(figsize=(6, 6))

status_pagamento = df["status_pagamento"].value_counts()

plt.pie(
    status_pagamento.values,
    labels=status_pagamento.index,
    autopct="%1.0f%%",
    colors=["green", "red"],
    startangle=90
)
plt.title("Status de Pagamento dos Pedidos")

plt.savefig(r"C:\Users\mateu\Downloads\CP1_Dynamic_Programming\grafico4_pagamento.png")
plt.close()
print("Grafico 4 salvo: grafico4_pagamento.png")

# -----------------------------------------------------------
# Resumo das complexidades Big O
# -----------------------------------------------------------
print()
print("=== COMPLEXIDADE BIG O ===")
print("Leitura do CSV:                   O(n)")
print("Criacao da lista de tuplas:       O(n)")
print("Ordenacao com sorted():           O(n log n)")
print("append() e popleft() no deque:    O(1) cada")
print("Calculo recursivo do total:       O(n)")
print("Graficos:                         O(n)")
