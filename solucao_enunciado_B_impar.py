# Checkpoint 1 - Enunciado B
# Sistema de fretes e entregas
# Priorizar cargas por custo, prazo e criticidade da rota
# Estruturas usadas: lista, tupla, dicionario, deque, DataFrame
# Tambem tem: ordenacao, recursao e graficos

import sys
sys.stdout.reconfigure(encoding="utf-8")  # evita erro de encoding no windows

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # necessario pra salvar grafico sem abrir janela
import matplotlib.pyplot as plt
from collections import deque

# -----------------------------------------------------------
# Lendo o arquivo CSV com os dados das entregas
# -----------------------------------------------------------

df = pd.read_csv(r"C:\Users\mateu\Downloads\Check_point_1_dados_logistica_RA_final impar (1).csv")

print("=== DADOS DAS ENTREGAS ===")
print(df)
print()

# -----------------------------------------------------------
# Criando uma LISTA de TUPLAS com as entregas
# Tupla pq os dados de cada entrega sao fixos, nao precisam mudar
# Posicoes: (id, origem, destino, tipo_carga, peso, frete, prazo, prioridade, rota, transportadora)
# -----------------------------------------------------------

lista_entregas = []

for i, row in df.iterrows():
    entrega = (
        row["entrega_id"],
        row["origem"],
        row["destino"],
        row["tipo_carga"],
        row["peso_kg"],
        row["valor_frete"],
        row["prazo_dias"],
        row["prioridade_cliente"],
        row["situacao_rota"],
        row["transportadora"]
    )
    lista_entregas.append(entrega)

print("=== ENTREGAS EM FORMATO DE TUPLA ===")
print("(id, origem, destino, carga, peso, frete, prazo, prioridade, rota, transportadora)")
for e in lista_entregas:
    print(e)
print()

# -----------------------------------------------------------
# DICIONARIOS
# Uso dicionarios pra mapear os valores categoricos em numeros
# assim consigo ordenar as entregas por prioridade
# -----------------------------------------------------------

# situacao da rota: critica = mais urgente (1), livre = menos urgente (3)
peso_rota = {
    "critica": 1,
    "atencao": 2,
    "livre": 3
}

# prioridade do cliente: vip tem preferencia
peso_prioridade = {
    "vip": 1,
    "normal": 2
}

# cores pra usar nos graficos
cores_rota = {
    "critica": "red",
    "atencao": "orange",
    "livre": "green"
}

# dicionario pra guardar estatisticas de cada transportadora
stats_transportadora = {}

for entrega in lista_entregas:
    transp = entrega[9]  # transportadora esta na posicao 9

    # se a transportadora ainda nao foi adicionada, cria o registro
    if transp not in stats_transportadora:
        stats_transportadora[transp] = {
            "num_entregas": 0,
            "total_frete": 0,
            "total_peso": 0
        }

    # atualiza os valores
    stats_transportadora[transp]["num_entregas"] = stats_transportadora[transp]["num_entregas"] + 1
    stats_transportadora[transp]["total_frete"] = stats_transportadora[transp]["total_frete"] + entrega[5]
    stats_transportadora[transp]["total_peso"] = stats_transportadora[transp]["total_peso"] + entrega[4]

print("=== ESTATISTICAS POR TRANSPORTADORA ===")
for transp in stats_transportadora:
    info = stats_transportadora[transp]
    print("Transportadora", transp, ": ",
          info["num_entregas"], "entregas |",
          "R$", info["total_frete"], "em fretes |",
          info["total_peso"], "kg")
print()

# -----------------------------------------------------------
# Ordenacao das entregas
# Criterios em ordem de importancia:
#   1. Situacao da rota (critica primeiro)
#   2. Prioridade do cliente (vip primeiro)
#   3. Prazo (menor prazo primeiro - mais urgente)
#   4. Valor do frete (maior frete primeiro - mais rentavel)
# O(n log n) - Python usa Timsort
# -----------------------------------------------------------

def criterio_ordenacao(entrega):
    rota = peso_rota[entrega[8]]        # situacao_rota na posicao 8
    cliente = peso_prioridade[entrega[7]]  # prioridade_cliente na posicao 7
    prazo = entrega[6]                  # prazo_dias na posicao 6
    frete = -entrega[5]                 # negativo pra maior frete vir primeiro
    return (rota, cliente, prazo, frete)

lista_ordenada = sorted(lista_entregas, key=criterio_ordenacao)

print("=== ENTREGAS ORDENADAS POR PRIORIDADE ===")
for e in lista_ordenada:
    print("ID:", e[0], "| Rota:", e[1], "->", e[2], "| Situacao:", e[8],
          "| Cliente:", e[7], "| Prazo:", e[6], "dias | Frete: R$", e[5])
print()

# -----------------------------------------------------------
# DEQUE - Fila de despacho
# As entregas sao colocadas na fila na ordem de prioridade
# e retiradas uma por vez pra processar (FIFO)
# append -> O(1) | popleft -> O(1)
# -----------------------------------------------------------

fila_despacho = deque()

print("=== ADICIONANDO ENTREGAS NA FILA ===")
for entrega in lista_ordenada:
    fila_despacho.append(entrega)
    print("Entrega #" + str(entrega[0]), entrega[1], "->", entrega[2],
          "| Rota:", entrega[8], "| Cliente:", entrega[7])

print()
print("Total de entregas na fila:", len(fila_despacho))
print()

# processando as entregas uma por uma
print("=== PROCESSANDO FILA DE DESPACHO ===")
print("-" * 55)

seq = 1
log_despacho = []  # lista de dicionarios com historico

while len(fila_despacho) > 0:
    e = fila_despacho.popleft()  # retira o primeiro da fila

    print("Seq:", seq, "| #" + str(e[0]), e[1], "->", e[2],
          "| Carga:", e[3], "| Peso:", e[4], "kg | Frete: R$", e[5],
          "| Prazo:", e[6], "dias | Transp:", e[9])

    registro = {
        "seq": seq,
        "entrega_id": e[0],
        "origem": e[1],
        "destino": e[2],
        "tipo_carga": e[3],
        "peso_kg": e[4],
        "valor_frete": e[5],
        "prazo_dias": e[6],
        "prioridade_cliente": e[7],
        "situacao_rota": e[8],
        "transportadora": e[9]
    }
    log_despacho.append(registro)
    seq = seq + 1

print()

# converte o historico em DataFrame
df_despacho = pd.DataFrame(log_despacho)
print("=== LOG DE DESPACHO (DataFrame) ===")
print(df_despacho)
print()

# -----------------------------------------------------------
# RECURSAO - calcula o custo total de frete de forma recursiva
# Caso base: indice chegou no final da lista -> retorna 0
# Caso recursivo: frete atual + resultado da chamada pro proximo
# Complexidade: O(n)
# -----------------------------------------------------------

def calcular_total_frete(lista, indice=0):
    # caso base
    if indice == len(lista):
        return 0

    # caso recursivo
    return lista[indice]["valor_frete"] + calcular_total_frete(lista, indice + 1)

# outra funcao recursiva pra calcular o peso total
def calcular_total_peso(lista, indice=0):
    # caso base
    if indice == len(lista):
        return 0

    # caso recursivo
    return lista[indice]["peso_kg"] + calcular_total_peso(lista, indice + 1)

total_frete = calcular_total_frete(log_despacho)
total_peso = calcular_total_peso(log_despacho)

print("Custo total de frete (recursao): R$", total_frete)
print("Peso total carregado (recursao):", total_peso, "kg")
print()

# -----------------------------------------------------------
# GRAFICOS
# -----------------------------------------------------------

# Grafico 1: valor de frete por ordem de despacho
plt.figure(figsize=(8, 5))

sequencias = []
fretes = []
cores_barras = []
rotulos = []

for registro in log_despacho:
    sequencias.append(registro["seq"])
    fretes.append(registro["valor_frete"])
    cores_barras.append(cores_rota[registro["situacao_rota"]])
    rotulos.append("#" + str(registro["entrega_id"]) + "\n" + registro["origem"] + "->" + registro["destino"])

plt.bar(sequencias, fretes, color=cores_barras, edgecolor="black")
plt.title("Valor de Frete por Ordem de Despacho")
plt.xlabel("Entrega")
plt.ylabel("Valor do Frete (R$)")
plt.xticks(sequencias, rotulos, fontsize=8)

# adiciono legenda manual explicando as cores
from matplotlib.patches import Patch
legenda = [
    Patch(color="red", label="critica"),
    Patch(color="orange", label="atencao"),
    Patch(color="green", label="livre")
]
plt.legend(handles=legenda, title="Situacao da Rota")
plt.tight_layout()

plt.savefig(r"C:\Users\mateu\Downloads\CP1_Dynamic_Programming\grafico1_fretes.png")
plt.close()
print("Grafico 1 salvo: grafico1_fretes.png")

# Grafico 2: peso total por transportadora
plt.figure(figsize=(7, 5))

transportadoras = list(stats_transportadora.keys())
pesos = []
for t in transportadoras:
    pesos.append(stats_transportadora[t]["total_peso"])

plt.bar(transportadoras, pesos, color=["steelblue", "mediumpurple", "darkorange"], edgecolor="black")
plt.title("Peso Total por Transportadora")
plt.xlabel("Transportadora")
plt.ylabel("Peso Total (kg)")

for i in range(len(transportadoras)):
    plt.text(i, pesos[i] + 2, str(pesos[i]) + " kg", ha="center")

plt.savefig(r"C:\Users\mateu\Downloads\CP1_Dynamic_Programming\grafico2_peso.png")
plt.close()
print("Grafico 2 salvo: grafico2_peso.png")

# Grafico 3: prazo de entrega por sequencia de despacho
plt.figure(figsize=(8, 5))

prazos = []
for registro in log_despacho:
    prazos.append(registro["prazo_dias"])

plt.plot(sequencias, prazos, marker="o", color="steelblue", linewidth=2)
plt.title("Prazo de Entrega por Sequencia de Despacho")
plt.xlabel("Sequencia de Despacho")
plt.ylabel("Prazo (dias)")
plt.xticks(sequencias)
plt.grid(axis="y", linestyle="--", alpha=0.5)

# coloco o valor em cima de cada ponto
for i in range(len(sequencias)):
    plt.text(sequencias[i], prazos[i] + 0.1, str(prazos[i]) + "d", ha="center", fontsize=9)

plt.savefig(r"C:\Users\mateu\Downloads\CP1_Dynamic_Programming\grafico3_prazos.png")
plt.close()
print("Grafico 3 salvo: grafico3_prazos.png")

# Grafico 4: pizza com distribuicao por situacao de rota
plt.figure(figsize=(6, 6))

contagem_rota = df["situacao_rota"].value_counts()

cores_pizza = []
for rota in contagem_rota.index:
    cores_pizza.append(cores_rota[rota])

plt.pie(contagem_rota.values, labels=contagem_rota.index, autopct="%1.0f%%", colors=cores_pizza, startangle=90)
plt.title("Distribuicao por Situacao da Rota")

plt.savefig(r"C:\Users\mateu\Downloads\CP1_Dynamic_Programming\grafico4_rotas.png")
plt.close()
print("Grafico 4 salvo: grafico4_rotas.png")

# -----------------------------------------------------------
# Resumo das complexidades Big O
# -----------------------------------------------------------
print()
print("=== COMPLEXIDADE BIG O ===")
print("Leitura do CSV:                   O(n)")
print("Criacao da lista de tuplas:       O(n)")
print("Agrupamento no dicionario:        O(n)")
print("Ordenacao com sorted():           O(n log n)")
print("append() e popleft() no deque:    O(1) cada")
print("Recursao para frete e peso:       O(n) cada")
print("Graficos:                         O(n)")
