# Relatório de desempenho da linha de base — AMS

**Projeto:** AMS · Assistente de Manutenção Segura · **Data:** [preencha a data da sua medição]

## 1. A métrica primária

**Falhas antecipadas:** proporção das falhas reais que o agente classificou como risco alto.

> falhas antecipadas = (casos com falha e risco previsto = `alto`) ÷ (total de casos com falha)

Um caso conta como "com falha" quando `Machine failure = 1` no conjunto. Todos eles têm risco correto `alto`. A métrica privilegia a revocação porque o erro grave do domínio é não antecipar uma falha: a máquina é tratada como rotina e o técnico pode intervir sem o bloqueio adequado.

Métrica secundária, **alarmes falsos:** casos sem falha classificados como risco alto, sobre o total de casos sem falha. A razão de olhar a secundária é impedir que o agente "melhore" a primária só classificando tudo como alto.

## 2. O valor

```
Métrica primária — falhas antecipadas: 14/20 = 0.7
Secundária — alarmes falsos:            0/10 = 0.0
Acerto geral (apenas para referência):  24/30 = 0.8
```

## 3. O conjunto

- **Arquivo:** `30_novos_casos_ams.csv` (pasta `data\dados` do projeto).
- **Tamanho:** 30 casos, sendo 20 com falha e 10 sem falha.
- **Origem:** conjunto **sintético** (`origem = sintetico`), montado para a avaliação do baseline. Não é o conjunto de reserva do pacote nem uma amostra do AI4I original. Os casos não têm período, e a ordem é dada pelo UDI (série 90xxx).
- **Distribuição pelos rótulos:** os 10 casos sem falha têm risco correto `baixo` e são todos fáceis (leituras normais, desgaste baixo, os três tipos de máquina). Os 20 com falha têm risco correto `alto`, entre eles casos atípicos (falha aleatória sem sinal nos sensores).

## 4. Onde o agente erra

```
Falhas que o agente não antecipou:
  C52 (UDI 90052, falha)
  C53 (UDI 90053, falha)
  C55 (UDI 90055, falha)
  C59 (UDI 90059, falha)
  C67 (UDI 90067, atipico)
  C70 (UDI 90070, atipico)
```

**O padrão.** Os seis erros são do mesmo tipo: falhas perdidas. Não há nenhum alarme falso, e isso ocorre porque os 10 casos sem falha são todos fáceis. Os erros se dividem em dois grupos:

- **Falhas sem rastro nos sensores (C55, C67 e C70):** são falhas aleatórias (RNF), com leituras dentro da faixa normal.
- **Falhas de sinal fraco (C52, C53 e C59):** C52 e C59 estão rotulados como falha por dissipação de calor, mas têm diferença de temperatura de 10,8 K, acima do limite de 8,6 K da regra. C53 está rotulado como falha de potência, mas tem cerca de 3.660 W, acima do mínimo de 3.500 W. Nenhuma leitura cruza o limiar do agente.

**A hipótese.** O agente usa limiares fixos sobre a leitura atual e não tem memória. Ele só enxerga o que o sensor mostra com clareza naquele instante. Falhas aleatórias não deixam sinal algum, e as de sinal fraco não violam nenhuma regra, então o rótulo vem de uma condição que o agente não observa. O que falta é contexto que o AI4I não traz: o histórico de cada máquina e a tendência das leituras ao longo do tempo. É isso que um agente baseado em modelo (D10) teria de incorporar. Como o conjunto não contém casos difíceis perto dos limiares, o 0 de alarmes falsos é pouco informativo e deve ser lido com essa ressalva.

## 5. A tabela comparativa de busca (item 4 da N2)

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| largura | 20.0 | 1 | 11 | 140 | 2 | 0.0006 |
| custo_uniforme | 17.1 | 6 | 1488 | 2450 | 7 | 0.0063 |
| profundidade_limitada(limite=32) | 17.6 | 7 | 8 | 28 | 7 | 0.0001 |
| aprofundamento_iterativo(limite=32) | 20.0 | 1 | 12 | 10 | 1 | 0.0001 |
| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| gulosa[admissivel] | 20.0 | 1 | 2 | 14 | 1 | 0.0002 |
| a_estrela[admissivel] | 17.1 | 6 | 1307 | 2338 | 6 | 0.0208 |
| gulosa[inadmissivel] | 20.0 | 1 | 2 | 14 | 1 | 0.0001 |
| a_estrela[inadmissivel] | 20.0 | 1 | 2 | 14 | 1 | 0.0001