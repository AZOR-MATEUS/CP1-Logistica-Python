# CP1 — Simulação de Logística com Estruturas de Dados em Python

> Checkpoint 1 — Disciplina de Estruturas de Dados  
> Curso: Engenharia de Software  
> Organização: AZOR-MATEUS

---

## Sobre o Projeto

Este projeto foi desenvolvido como parte do Checkpoint 1 da disciplina. O objetivo foi aplicar na prática conceitos de estruturas de dados — listas, tuplas, dicionários, deques e DataFrames — em um contexto real de logística brasileira.

O projeto é dividido em dois enunciados, cada um resolvido em um arquivo separado:

| Arquivo | Enunciado | Tema |
|---|---|---|
| `solucao_enunciado_A_par.py` | A — RA final PAR | Simulação de centro de distribuição com fila de pedidos |
| `solucao_enunciado_B_impar.py` | B — RA final ÍMPAR | Sistema de fretes e entregas com priorização de cargas |

---

## Como Executar

**Requisitos:**
- Python 3.10 ou superior
- Bibliotecas: `pandas` e `matplotlib`

**Instalação das dependências:**
```bash
pip install pandas matplotlib
```

**Executando os scripts:**
```bash
python -X utf8 solucao_enunciado_A_par.py
python -X utf8 solucao_enunciado_B_impar.py
```

> A flag `-X utf8` é necessária no Windows para evitar erros de encoding com caracteres especiais.

Os gráficos são salvos automaticamente como arquivos `.png` na mesma pasta do script.

---

## Enunciado A — Centro de Distribuição com Fila de Pedidos

### O que o programa faz

O script lê um arquivo CSV com pedidos de um centro de distribuição e simula o processo de expedição desses pedidos. A ideia é que os pedidos mais urgentes e de maior valor saiam primeiro.

### Fluxo do programa

```
CSV → DataFrame → Lista de Tuplas → Ordenação → Deque (fila) → Processamento → Log (DataFrame) → Gráficos
```

### Estruturas de dados utilizadas

**Tupla** — cada pedido é armazenado como uma tupla com 7 campos:
```
(pedido_id, produto, urgencia, valor_total, modal, cidade_destino, tempo_estimado_horas)
```
Escolhi tupla porque os dados de um pedido não devem ser alterados depois de criados. A tupla garante isso por ser imutável.

**Lista** — usada para guardar todas as tuplas de pedidos e também para construir o histórico de processamento. A lista foi escolhida por ser a estrutura mais simples para armazenar e percorrer uma coleção de elementos em sequência.

**Dicionários** — foram usados três dicionários:
- `prioridade_urgencia` → mapeia `"alta"`, `"media"`, `"baixa"` para números (1, 2, 3), permitindo ordenar por urgência
- `cores_urgencia` → mapeia cada nível de urgência para uma cor, usado nos gráficos
- `pedidos_por_urgencia` → agrupa os pedidos separados por nível de urgência

**Deque** — a fila de expedição foi implementada com `deque` da biblioteca `collections`. O motivo é que o deque permite adicionar elementos no final (`append`) e remover do início (`popleft`) com complexidade **O(1)**, enquanto uma lista comum teria custo **O(n)** para remover do início.

**DataFrame** — usado tanto para ler o CSV quanto para registrar o log de expedição de forma tabular e organizada.

### Critério de ordenação

Os pedidos são ordenados com dois critérios:
1. **Urgência** (alta → media → baixa): pedidos urgentes saem primeiro
2. **Valor total** (maior → menor): em caso de empate na urgência, o pedido de maior valor tem prioridade

### Recursão

A função `calcular_valor_total` calcula o valor somado de todos os pedidos expedidos de forma recursiva:
- **Caso base:** quando o índice chega ao final da lista, retorna 0
- **Caso recursivo:** retorna o valor do pedido atual somado com a chamada para o próximo índice

### Gráficos gerados

| Arquivo | Conteúdo |
|---|---|
| `grafico1_urgencia.png` | Quantidade de pedidos por nível de urgência |
| `grafico2_modal.png` | Valor total movimentado por modal de transporte |
| `grafico3_tempo.png` | Tempo estimado de cada pedido na ordem de saída |
| `grafico4_pagamento.png` | Distribuição do status de pagamento |

---

## Enunciado B — Sistema de Fretes e Entregas

### O que o programa faz

O script lê um arquivo CSV com entregas de um sistema de fretes e decide a ordem em que cada carga deve ser despachada, levando em conta a criticidade da rota, o tipo de cliente, o prazo e o valor do frete.

### Fluxo do programa

```
CSV → DataFrame → Lista de Tuplas → Dicionários de peso → Ordenação multicritério → Deque → Processamento → Log (DataFrame) → Gráficos
```

### Estruturas de dados utilizadas

**Tupla** — cada entrega é armazenada como uma tupla com 10 campos:
```
(entrega_id, origem, destino, tipo_carga, peso_kg, valor_frete, prazo_dias, prioridade_cliente, situacao_rota, transportadora)
```
Assim como no Enunciado A, a tupla foi escolhida pela imutabilidade, já que os dados de uma entrega não devem ser modificados durante o processamento.

**Lista** — usada para armazenar as tuplas de entregas e o histórico de despacho (como lista de dicionários).

**Dicionários** — quatro dicionários foram utilizados:
- `peso_rota` → converte `"critica"`, `"atencao"`, `"livre"` em valores numéricos para ordenação
- `peso_prioridade` → converte `"vip"` e `"normal"` em valores numéricos
- `cores_rota` → define as cores por situação de rota para os gráficos
- `stats_transportadora` → acumula estatísticas de cada transportadora (total de entregas, frete e peso)

**Deque** — a fila de despacho segue a mesma lógica do Enunciado A: as entregas entram em ordem de prioridade e são retiradas do início uma por vez.

**DataFrame** — utilizado para leitura do CSV e exibição tabular do log de despacho.

### Critério de ordenação (multicritério)

As entregas são ordenadas por quatro critérios em cascata:
1. **Situação da rota** (critica → atencao → livre): rotas comprometidas têm prioridade máxima
2. **Prioridade do cliente** (vip → normal): clientes VIP passam à frente em caso de empate
3. **Prazo** (menor → maior): prazo mais apertado = mais urgente
4. **Valor do frete** (maior → menor): em último caso, o frete mais rentável tem preferência

### Recursão

Duas funções recursivas foram implementadas:
- `calcular_total_frete` → soma o valor de frete de todas as entregas
- `calcular_total_peso` → soma o peso total de todas as cargas despachadas

Ambas seguem o mesmo padrão: caso base retorna 0 quando o índice ultrapassa o tamanho da lista; caso recursivo soma o valor atual com o resultado da chamada para o próximo índice.

### Gráficos gerados

| Arquivo | Conteúdo |
|---|---|
| `grafico1_fretes.png` | Valor de frete por ordem de despacho (colorido por situação de rota) |
| `grafico2_peso.png` | Peso total transportado por cada transportadora |
| `grafico3_prazos.png` | Prazo de entrega por sequência de despacho |
| `grafico4_rotas.png` | Distribuição das entregas por situação de rota |

---

## Análise de Complexidade (Big O)

| Operação | Complexidade | Justificativa |
|---|---|---|
| Leitura do CSV | O(n) | Percorre cada linha uma vez |
| Criação da lista de tuplas | O(n) | Um loop para cada pedido/entrega |
| Agrupamento em dicionário | O(n) | Um loop para cada elemento |
| Ordenação com `sorted()` | O(n log n) | Python usa o algoritmo Timsort |
| `append()` no deque | O(1) | Inserção no final é constante |
| `popleft()` no deque | O(1) | Remoção no início é constante |
| Recursão (total/peso) | O(n) | Passa uma vez por cada elemento |
| Geração dos gráficos | O(n) | Percorre os dados uma vez |

> O ponto mais custoso do programa é a ordenação com O(n log n). Para os dados atuais (5 registros), isso não faz diferença, mas em um sistema real com milhares de pedidos, a escolha do algoritmo de ordenação passaria a ser crítica.

---

## Hipóteses e Considerações

Durante o desenvolvimento deste projeto, algumas decisões precisaram ser tomadas com base em hipóteses sobre como o sistema funcionaria em um cenário real.

**1. Por que tupla e não dicionário para os pedidos?**  
Optei por usar tupla para representar cada pedido porque, uma vez que um pedido é registrado no sistema, seus dados não devem ser alterados. A imutabilidade da tupla serve como uma proteção natural contra modificações acidentais. Se fosse necessário atualizar dados dos pedidos durante o processamento, eu usaria dicionários.

**2. Por que deque e não lista para a fila?**  
A lista do Python tem custo O(n) para remover o primeiro elemento (porque precisa deslocar todos os outros). O deque resolve isso com O(1). Em um sistema com muitos pedidos sendo processados em sequência, essa diferença de eficiência seria muito relevante.

**3. Hipótese sobre os critérios de urgência**  
Assumi que a urgência declarada no cadastro do pedido é o critério mais importante, e que dentro do mesmo nível de urgência, o pedido de maior valor financeiro deve ter prioridade. Essa decisão foi baseada na lógica de que o centro de distribuição tem interesse tanto em atender o cliente urgente quanto em garantir a saída de itens de maior valor.

**4. Hipótese sobre a criticidade da rota (Enunciado B)**  
No sistema de fretes, a situação da rota foi considerada o critério de maior peso porque uma rota "crítica" indica algum tipo de impedimento ou risco que pode piorar com o tempo. Faz mais sentido despachar primeiro as cargas para rotas comprometidas do que deixar a situação se agravar.

**5. Limitação do dataset**  
Os arquivos CSV utilizados contêm apenas 5 registros cada. O programa funciona corretamente, mas não foi possível testar o comportamento com volumes maiores de dados. Em um cenário real, seria necessário avaliar a performance para centenas ou milhares de registros, e possivelmente usar estruturas mais otimizadas como heaps (filas de prioridade) para a ordenação contínua.

**6. Recursão vs. loop simples**  
A recursão foi utilizada para o cálculo dos totais por ser um requisito do trabalho. Em termos práticos, um simples `sum()` ou um loop `for` seria mais eficiente e evitaria o risco de estouro de pilha (`RecursionError`) em listas muito grandes. O Python tem um limite padrão de ~1000 chamadas recursivas.

---

## Estrutura de Arquivos

```
CP1-Logistica-Python/
│
├── solucao_enunciado_A_par.py       # Enunciado A: centro de distribuição
├── solucao_enunciado_B_impar.py     # Enunciado B: sistema de fretes
│
├── grafico1_urgencia.png            # Gráfico A: pedidos por urgência
├── grafico2_modal.png               # Gráfico A: valor por modal
├── grafico3_tempo.png               # Gráfico A: tempo estimado por pedido
├── grafico4_pagamento.png           # Gráfico A: status de pagamento
│
├── grafico1_fretes.png              # Gráfico B: frete por despacho
├── grafico2_peso.png                # Gráfico B: peso por transportadora
├── grafico3_prazos.png              # Gráfico B: prazo por despacho
└── grafico4_rotas.png               # Gráfico B: distribuição por rota
```

---

## Tecnologias Utilizadas

- **Python 3.13**
- **pandas** — leitura de CSV e manipulação de dados tabulares
- **matplotlib** — geração dos gráficos
- **collections.deque** — estrutura de fila eficiente
