# Pares que surpreenderam — Laboratório 01

> O slide 19 do D3-E1 pede DOIS casos anotados: um par PRÓXIMO sem razão aparente e um par DISTANTE que deveria estar junto. Eles voltam na D7, quando a turma montar o próprio índice de recuperação — escreva aqui e guarde este arquivo no seu repositório.

## Um par PRÓXIMO sem razão aparente

- Índices do par: (68, 107)
- As duas frases:
  - primeira: A malha de controle de temperatura do forno…
  - segunda: A chaminé do forno precisa de inspeção de r…
- Cosseno medido: 0.8034
- Por que essa proximidade surpreendeu:

R: A proximidade surpreendeu porque, apesar de as frases tratarem de componentes e atividades de manutenção diferentes, o modelo identificou uma alta similaridade semântica entre elas. Isso pode ter ocorrido devido ao compartilhamento de termos relacionados ao forno, à manutenção industrial e aos equipamentos, fazendo com que os vetores apresentassem uma distância pequena no espaço semântico.

## Um par DISTANTE que deveria estar junto

- Índices do par: (174, 197)
- As duas frases:
  - primeira: A parada anual da usina não está planejada …
  - segunda: O inventário de sobressalentes críticos foi…
- Cosseno medido: -0.1462
- Por que essa distância surpreendeu:

R: A distância surpreendeu porque as duas frases estão relacionadas ao planejamento e à gestão da manutenção industrial. A parada anual da usina depende de um planejamento adequado, incluindo a disponibilidade de peças e sobressalentes críticos. Mesmo existindo uma relação contextual entre os assuntos, o modelo identificou uma similaridade muito baixa, indicando uma possível dificuldade em reconhecer relações semânticas indiretas.

## O que a comparação com NORMALIZAR = True mudou

- Alguma ordem mudou? De qual par:

 Os pares continuaram apresentando a mesma classificação de proximidade o cosseno não muda nada e distância eucl se altera