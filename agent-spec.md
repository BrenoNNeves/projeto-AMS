# agent-spec.md — modelo do meu agente

<!--
Este arquivo é para preencher, não para ler e devolver. As perguntas de cada
seção estão em comentário como este: elas não aparecem na pré-visualização,
aparecem no editor. Responda ABAIXO de cada seção, apagando nada delas.

As seções que ainda não foram vistas em aula ficam de pé, com a linha
"quando se preenche" dizendo o encontro em que isso acontece. O documento
cresce a cada laboratório — o de hoje é o primeiro.

Preencha com exemplos concretos do SEU domínio. Uma linha que funcionaria
para qualquer empresa é uma linha genérica — o exemplo do seu segmento
(agente-spec-exemplo.pdf, no mesmo pacote) mostra o contraste.
-->

**Domínio:** [título curto do domínio, do dominio.md da D1]
**Autor(a):** Breno Neves · **Última revisão:** 13/10/2026

---

## 1. PEAS

-->
**Quando se preenche:** no Laboratório 01, hoje. Refinado na Atividade Orientada.

**Performance:**

O desempenho vai partir do pincipio se o agente esta classificando corretamente as ordens de serviço, tendo a formula a porcentagem de acertos, meta de aceito é de 95% hoje (70%)
Fórmula:

Taxa de acerto = (Número de ordens com todas as decisões corretas / Total de ordens avaliadas) × 100


**Environment:**

sensores de temperatura, rotação, torque e desgaste de ferramenta, tecnico responsavel

**Actuators:**

Classificar o risco como medio/baixo/alto indicar quais normas regulamentadas são aplicadas e se é necessario realizar um bloqueio. Além disso, devera apresentar uma justificativa clara para suas recomendações, permitindo que o tecnico entenda os fatores considerados na análise. Os resultados serão organizados em um objeto estruturado chamado AvaliacaoRisco, facilitando a validação e o uso das informações por outros componentes do sistema.

**Sensors:**

O agente utilizará as leituras de temperatura, rotação, torque e desgaste de ferramenta, além dos dados disponíveis sobre a máquina e seu histórico de falhas. Na etapa inicial do projeto, essas informações serão obtidas principalmente do dataset público AI4I 2020 Predictive Maintenance Dataset.

Também serão utilizadas as descrições textuais das ordens de serviço, que ajudam a compreender qual intervenção será realizada e quais condições precisam ser consideradas.

---

## 2. O ambiente em sete dimensões

<!--
Perguntas que guiam o preenchimento (uma por dimensão):
  - Observabilidade: existe algo que muda a decisão e o agente não mede?
  - Número de agentes: existe alguém cujas ações mudam o seu resultado?
    Um humano que reage ao agente conta.
  - Determinismo: a mesma ação no mesmo estado dá sempre o mesmo efeito?
  - Episódico ou sequencial: a decisão de agora afeta as decisões seguintes?
  - Estático ou dinâmico: o ambiente muda enquanto o agente delibera?
  - Discreto ou contínuo: estados e ações são contáveis?
  - Conhecido ou desconhecido: o agente sabe de antemão as regras? (Trata do
    que ele SABE, não do que ele VÊ.)
  Cada classificação vem com uma frase de justificativa — a etiqueta sozinha
  não vale nada.
-->
- **Observabilidade: parcialmente observável.** Em cada solicitação, o AMS recebe as leituras disponíveis (temperaturas, rotação, torque e desgaste), a identificação/tipo da máquina e a descrição da ordem de serviço. Isso não revela necessariamente o histórico completo de manutenção, o estado de outros componentes, as condições do local nem como o procedimento será executado; esses fatores podem alterar o risco e a aplicação das normas.
- **Determinismo: estocástico.** As mesmas leituras não garantem o mesmo resultado: falhas podem ter causas distintas e são minoria no AI4I 2020. O conjunto de dados mostra associações, não uma regra determinística que permita afirmar que uma máquina falhará ou não.
- **Número de agentes: multiagente.** O AMS recomenda, mas o técnico responsável decide se segue a recomendação e executa a intervenção; o supervisor pode revisar o parecer. As ações humanas influenciam o desfecho, portanto o sistema não atua isoladamente.
- **Episódico ou sequencial: sequencial no domínio operacional.** A avaliação de uma ordem é uma unidade, mas a decisão do técnico afeta o estado futuro: fazer manutenção pode reduzir o desgaste, enquanto adiar uma intervenção pode levar a novas leituras ou ordens. O protótipo atual recebe registros e não simula essas transições; essa dimensão descreve o uso pretendido na planta.
- **Estático ou dinâmico: dinâmico na planta.** Enquanto o AMS analisa uma leitura, a máquina pode continuar operando e seu estado pode mudar. Como o protótipo avalia um retrato dos dados recebido na solicitação, a recomendação precisa ser revista se houver mudança relevante antes da intervenção.
- **Discreto ou contínuo: misto, com variáveis contínuas.** Temperaturas, rotação, torque e desgaste são medidas numéricas; o tipo de produto, os níveis de risco, as normas selecionadas e a decisão de bloqueio são categorias discretas. A saída do AMS, portanto, é discreta, embora parte do estado observado seja numérico.
- **Conhecido ou desconhecido: desconhecido quanto à relação entre estado e falha.** O formato da entrada e da saída é definido, mas a relação entre as leituras e a ocorrência de falhas não é conhecida de antemão e precisa ser estimada e validada com dados. A descrição da ordem também não basta para determinar com certeza quais exigências de segurança se aplicam; recomendações normativas precisam ser verificadas contra as normas vigentes e pelo responsável técnico.


---

## 3. Tipo de agente pretendido

<!--
Perguntas que guiam o preenchimento:
  - O tipo mais simples que resolve: reativo simples, baseado em modelo,
    baseado em objetivos, baseado em utilidade, ou um deles com aprendizagem?
  - A caracterização do ambiente (seção 2) é que decide — parcialmente
    observável elimina o reativo simples.
  - Justifique com a dimensão do ambiente que obriga a escolha.
-->
**Quando se preenche: Tipo 3** o agente deve entender o estado atual e qual deve ser o desejado, deve entender como as maquinas estão e qual deve ser o rumo que deve ser tomado, parar, acionar tecnico ou outra, sempre buscando qual a sequencia ideal para chegar ao objetivo especificado.

---

## 4. Medida de desempenho

<!--
Perguntas que guiam o preenchimento:
  - A fórmula do campo Performance, agora em definição operacional: como se
    calcula, passo a passo, sem ambiguidade?
  - Métrica primária e duas secundárias. As secundárias pegam o que a
    primária deixa passar (custo, latência, reabertura).
  - O conjunto de casos: de onde vêm, quantos são, de que período.
  - O limiar de sucesso e o valor de hoje.
-->
**Quando se preenche:** a fórmula começa no Laboratório 01; a definição
operacional completa — primária, secundárias, conjunto e limiar — é item da
Atividade Orientada.

**Métrica principal: acerto integral da ordem.** A ideia é comparar cada `AvaliacaoRisco`
com o parecer de referência, que foi revisado por um técnico e pelo supervisor. Uma ordem
só conta como certa quando bate o nível de risco, o conjunto de normas aplicáveis
e a decisão sobre bloqueio, os três juntos.

`acerto integral (%) = ordens com os três campos corretos / total de ordens avaliadas × 100`

Para começar vamos usar as **20 ordens que o cliente ja processou** no AMS,
com os pareceres de referência definidos pelo técnico e pelo supervisor
antes de rodar qualquer avaliação. Cada ordem errada derruba o resultado em 5 pontos, ou seja uma só ja deixa em 95%. 
Vale congelar essa versão do conjunto e anotar a data da revisão. Meta: **pelo menos 95%**.
Hoje estamos em **70%**, mas esse número vem só da estimativa que ficou registrada na seção PEAS,
então ainda falta confirmar no conjunto fixo e fazer a revisão.

**Métrica secundaria: sensibilidade para falhas.** Olhando só as leituras do
conjunto de teste do AI4I 2020 que têm falha registrada, calculamos quantas
o agente marca como risco alto.

`sensibilidade (%) = falhas reais sinalizadas como risco alto / total de falhas reais × 100`

O teste sera fixo e estratificado, com **2.000 registros (20% dos 10.000)**, e
sem misturar com os dados usados para ajustar o modelo. O arquivo
não traz um periodo individual de coleta, então não dá para falar em janela de tempo. Meta: **pelo menos 90%**.
Valor atual: **ainda não medido**. A acuracia da regra exploratoria de desgaste
não serve como medida dessa sensibilidade, e também não valida a resposta completa do agente.

**Métrica secundária: latência p95.** Pegamos os tempos totais registrados
das avaliações concluidas, ordenamos e olhamos o percentil 95. Vamos usar as mesmas **20
ordens em três rodadas online (60 avaliações no total)**, anotando a data e o modelo
configurado, e sem misturar com execuções offline. Meta: **p95 de até 30 segundos
por ordem**. Valor atual: **ainda não medido numa execução online instrumentada**,
já que o modo offline não representa a latência real do serviço.

---

## 5. Restrições

<!--
Perguntas que guiam o preenchimento:
  - Latência aceitável: a partir de quantos segundos a resposta perde valor?
  - Custo aceitável: quanto pode custar cada resolução?
  - O que o agente jamais pode fazer: a ação irreversível que ele não executa
    sozinho. Esta linha vira política em D12.
  - A troca que você aceita: quanto de qualidade por quanto de custo?
    Um exemplo numérico vale mais que a fórmula.
-->
**Quando se preenche:** na Atividade Orientada.

- **Latência aceitável:** até **30 segundos por ordem** no percentil 95, da
  submissão até a `AvaliacaoRisco` validada. Passou disso a recomendação já perde
  o valor pro técnico, então a execução tem que ser registrada como fora do limite e
  mandada pra análise humana.
- **Custo aceitável:** o limite inicial é de **US$ 0,01 por ordem** em chamadas
  online, calculado pelos tokens de entrada e saída e registrado em
  `custo_usd`. O modo offline custa US$ 0 em chamadas, mas não serve
  pra afirmar que o limite online foi atendido.
- **Ação proibida sem confirmação humana:** o AMS nunca pode parar ou
  religar uma máquina, aplicar ou retirar bloqueio e etiquetagem (LOTO), nem
  executar qualquer intervenção. Ele só recomenda, quem confirma e executa
  qualquer ação física é o técnico responsável.
- **Troca qualidade × custo:** numa comparação de modelos com um conjunto
  ampliado de pelo menos **100 ordens** (pra que a diferença em pontos
  percentuais possa ser medida), aceito baixar o acerto integral de 95% para
  **no minimo 93%** se o custo por ordem cair pelo menos **50%**, a sensibilidade
  para falhas continuar em **90% ou mais** e o limite de latência for mantido.
  Não aceito economia que aumente as falhas não sinalizadas, nesse caso mantenho
  o modelo mais seguro ou mando a ordem pra revisão humana.

---

## 6. Catálogo de ações

<!--
Perguntas que guiam o preenchimento:
  - Para cada ação: nome, entrada, saída, é reversível?, qual o risco se
    errar? As quatro colunas são obrigatórias — "baixo" não é descrição de
    risco.
  - Ações de leitura E de escrita: as que alteram o mundo são as que exigem
    cuidado, e são justamente as que mais ficam de fora.
  - Este catálogo é, literalmente, a lista de ferramentas que você vai
    implementar em D10.
-->
**Quando se preenche:** na Atividade Orientada — o pacote `D2-07` traz o
modelo da tabela e dois exemplos preenchidos.

[tabela: nome · entrada · saída · é reversível? · risco se
errar — ações de leitura e de escrita]

---

## 7. Formulação por busca
| Subproblema              | Estado                              | Ação                              | Custo                  |
|--------------------------|-------------------------------------|-----------------------------------|------------------------|
| Ordem de verificações   | Verificações feitas e resultados    | Fazer a próxima verificação       | Tempo da verificação   |
| Sequência de consultas  | O que já se sabe                    | Consultar uma fonte               | Latência da consulta   |
| Roteiro de conformidade | Itens verificados e pendências      | Verificar item ou resolver pendência | Esforço             |

verificar-formulacao — teste de sanidade da formulação de busca

— comum/problemas/consultas.py:PEQUENA
  1. estado é hashable ✅
  2. transição é função ✅
  3. ações estáveis na ordem ✅
  4. custo é positivo ou zero ✅
  5. objetivo é alcançável ✅
  6. estado não guarda o caminho ✅
  resumo: 6 ✅ · 0 ⚠️ · 0 ❌

  # As sete dimensões do agente `FONTES_PEQUENAS`

Problema: classe `Consultas`, instância `PEQUENA` (4 fatos, 5 fontes).
Pergunta: *"quantos dias de férias ainda tenho, já considerando a venda do saldo que pedi?"*

| Dimensão | Classificação | Por quê |
|---|---|---|
| **Observabilidade** | Totalmente observável | O estado é o conjunto de fatos já sabidos. O agente sempre sabe o que já tem e o que falta (`fatos_necessarios`). |
| **Número de agentes** | Agente único | Só o agente decide. As fontes são passivas e ninguém mais age sobre o resultado. |
| **Determinismo** | Determinístico | `transicao` é uma função pura: a mesma fonte, no mesmo estado, devolve sempre os mesmos fatos. A latência também é fixa. |
| **Episódico ou sequencial** | Sequencial | Cada consulta muda o que vale a pena consultar depois. Se o PDF do acordo já entregou a "janela mínima", a intranet vira redundante. O custo também se acumula ao longo do caminho. |
| **Estático ou dinâmico** | Estático | Fatos, fontes e latências não mudam enquanto o agente delibera. |
| **Discreto ou contínuo** | Discreto | Os estados são subconjuntos de 4 fatos (no máximo 2⁴ = 16) e as ações são 5 fontes. A latência é um número real, mas é só o custo da ação, não uma variável de estado. |
| **Conhecido ou desconhecido** | Conhecido | O agente conhece as regras: o que cada fonte fornece e quanto custa. Isso está declarado nas constantes. |
<!--
Perguntas que guiam o preenchimento:
  - Qual fatia do problema é um espaço de estados? (Nem toda fatia é — e
    reconhecer a que não é vale tanto quanto formular a que é.)
  - Os cinco componentes: estado inicial, ações, modelo de transição, teste
    de objetivo, custo de caminho. Comece pelo teste de objetivo.
  - O estado descreve a SITUAÇÃO, não a história de como se chegou nela.
-->
**Quando se preenche:** no Laboratório 03, sábado à tarde (encontro 2).

[os cinco componentes do seu subproblema: estado inicial,
ações, transição, teste de objetivo, custo]
