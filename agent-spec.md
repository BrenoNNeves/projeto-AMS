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

| Elemento | Descrição |
|---|---|
| **Quando se preenche** | O PEAS será elaborado no Laboratório 01 e poderá ser refinado posteriormente durante a Atividade Orientada. |
| **Performance (Desempenho)** | O desempenho do agente será medido pela sua capacidade de classificar corretamente as ordens de serviço. A meta inicial é alcançar uma taxa de acerto de 70%, com objetivo de evolução para 95%. A avaliação considera se todas as decisões tomadas para cada ordem estão corretas. **Fórmula:** Taxa de acerto = (Número de ordens com todas as decisões corretas / Total de ordens avaliadas) × 100. |
| **Environment (Ambiente)** | O ambiente envolve as máquinas industriais, os sensores responsáveis por coletar dados de temperatura, rotação, torque e desgaste de ferramentas, além dos técnicos responsáveis pelas intervenções de manutenção. |
| **Actuators (Atuadores)** | O agente deverá classificar o nível de risco da intervenção como baixo, médio ou alto, identificar as normas regulamentadoras aplicáveis e indicar se é necessário realizar o bloqueio da máquina (LOTO). Também deverá apresentar uma justificativa clara para cada recomendação, permitindo que o técnico compreenda os fatores considerados na análise. Os resultados serão organizados em um objeto estruturado chamado `AvaliacaoRisco`, facilitando sua validação e utilização por outros componentes do sistema. |
| **Sensors (Sensores)** | O agente utilizará leituras de temperatura, rotação, torque e desgaste de ferramentas, além de informações sobre a máquina e seu histórico de falhas. Na etapa inicial do projeto, esses dados serão obtidos principalmente do dataset público AI4I 2020 Predictive Maintenance Dataset. Também serão consideradas as descrições textuais das ordens de serviço, que ajudam a identificar qual intervenção será realizada e quais condições precisam ser avaliadas. |
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

### 6. Catálogo de ações

| Ação | Entrada | Saída | É reversível? | Risco se algo der errado |
|---|---|---|---|---|
| **Ler a ordem de serviço** | Número da ordem (`id_ordem`). | Identificação da máquina (UDI), descrição do serviço e data da solicitação. | Sim. Apenas consulta informações, sem alterar os dados. | Uma descrição incompleta ou pouco clara pode esconder riscos importantes. Por exemplo, um serviço no ventilador de um forro metálico pode envolver trabalho em altura (NR-35), mas essa necessidade pode passar despercebida. |
| **Consultar sensores e histórico de falhas da máquina** | Identificação da máquina (UDI). | Dados de temperatura, RPM, torque, desgaste de ferramentas e histórico recente de falhas. | Sim. Apenas consulta informações. | Consultar dados de outra máquina ou informações desatualizadas pode levar a uma avaliação incorreta. Além disso, no dataset AI4I, o campo de falha representa o que aconteceu naquele registro, e não uma previsão de falha futura. |
| **Consultar as normas de segurança (NR-10, NR-12 e NR-35)** | Tipo de intervenção e palavras-chave relacionadas ao serviço. | Trechos relevantes das normas, acompanhados de suas respectivas fontes. | Sim. Apenas consulta informações. | Utilizar trechos de normas desatualizadas ou que não se aplicam à atividade pode gerar recomendações incorretas e comprometer a segurança da intervenção. |
| **Avaliar a ordem de serviço (riscos, normas e LOTO)** | Leituras dos sensores, histórico de falhas, descrição do serviço e trechos das normas. | Objeto `AvaliacaoRisco`, contendo nível de risco, normas aplicáveis, necessidade de LOTO e justificativa da avaliação. | Sim. Apenas realiza cálculos e análises, sem executar ações externas. | Subestimar um risco pode fazer com que uma máquina prestes a apresentar uma falha seja tratada como se estivesse em condições normais. Por outro lado, superestimar os riscos pode gerar paradas desnecessárias e excesso de alertas, fazendo com que avisos importantes percam a atenção dos técnicos. |
| **Comunicar a avaliação ao técnico** | Objeto `AvaliacaoRisco` e um resumo da justificativa. | Recomendação de segurança enviada ao técnico responsável. | Parcialmente. A mensagem pode ser corrigida, mas o técnico pode já ter iniciado alguma ação com base na orientação recebida. | Uma orientação incorreta, como informar que o LOTO não é necessário quando deveria ser aplicado, pode levar o técnico a trabalhar com uma máquina energizada ou com partes móveis sem o devido bloqueio, aumentando o risco de acidentes graves. |
| **Encaminhar o caso ao supervisor de segurança** | Ordem de serviço, resultado da avaliação e motivo da necessidade de revisão, como risco elevado ou dúvida na interpretação de uma norma. | Caso encaminhado para análise e aprovação do supervisor. | Sim. O supervisor pode revisar a avaliação e devolver o caso para ajustes. | Encaminhar todos os casos para revisão pode sobrecarregar o supervisor e fazer com que alertas importantes sejam ignorados. Por outro lado, deixar de encaminhar situações realmente duvidosas pode permitir que uma intervenção insegura prossiga sem a devida análise. |
| **Registrar a avaliação para auditoria** | Objeto `AvaliacaoRisco`, dados utilizados na análise e horário do registro. | Registro permanente da avaliação, permitindo consultar o histórico e acompanhar possíveis correções. | Parcialmente. O registro original não pode ser apagado, mas é possível adicionar uma retificação. | Uma justificativa incorreta pode permanecer no histórico e comprometer futuras auditorias (D12). Também é importante evitar o armazenamento desnecessário de dados pessoais dos técnicos, respeitando os princípios da LGPD. |
| **Autorizar o início da intervenção** | Ordem de serviço avaliada, confirmação do bloqueio LOTO pelo técnico e aprovação do supervisor. | Autorização para iniciar a atividade no fluxo de manutenção. | Não. Depois que a intervenção começa, não é possível simplesmente desfazer seus efeitos. | É uma ação de alto risco, pois autorizar o início do serviço sem confirmar o bloqueio efetivo da máquina pode provocar uma partida inesperada e causar acidentes graves. A decisão final e a execução da intervenção devem permanecer sob responsabilidade humana. |

*Comentario que importa:* A maioria das ações vão ser realizadas pelo agente, porém a decisão final da manutenção devera ser feita com o tecnico responsavel

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
