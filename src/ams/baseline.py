#C:\Users\brenoPC\Desktop\CEDAG\projeto-AMS\data\raw\ai4i2020.csv

"""Laboratório 06 — o agente de linha de base do seu domínio.

O agente mais simples que resolve uma fatia do problema, SEM modelo de
linguagem: percepção (o registro), decisão (regras explícitas), ação (a
recomendação) e medida (a métrica primária do `agent-spec.md`, sobre 30
casos). O número que sai daqui é a linha de base contra a qual o agente de
D10 vai ser comparado — sem ela, "melhorou" é opinião.

Estrutura do slide 22 do D2-E4: uma função `decidir(registro, estado)` com
duas condições — a primeira REATIVA (só a percepção do instante) e a
segunda consultando ESTADO INTERNO (o que o agente já observou do mundo).
Quem caracterizou o ambiente como totalmente observável pode APAGAR a
segunda condição e ficar com um reativo simples — e registra a escolha na
análise, porque o tipo de agente é parte do que a rubrica avalia.

Como usar:
    1. adapte as regras (os TODOs) e os limiares ao SEU domínio;
    2. aponte CAMINHO_DOS_CASOS para o seu conjunto de 30 casos rotulados
       (ou deixe no conjunto de reserva — ver COMO-USAR-A-RESERVA.pdf);
    3. rode:  python medir.py
    4. quando o baseline estiver pronto, copie as funções para
       `src/<projeto>/baseline.py` — é o caminho que a entrega final cobra.

Este módulo roda de fábrica sobre o conjunto de reserva que viaja no
pacote: medida funcionando antes da primeira adaptação.
"""

from __future__ import annotations

import csv
from datetime import date as _date
from pathlib import Path

# --------------------------------------------------------------------------
# Configuração — a troca do dataset é UMA LINHA aqui (slide 29).
# --------------------------------------------------------------------------
CAMINHO_DOS_CASOS = "C:\\Users\\brenoPC\\Desktop\\CEDAG\\projeto-AMS\\data\\raw\\ai4i2020.csv"
# Troque pelo SEU conjunto quando estiver pronto:
# CAMINHO_DOS_CASOS = "dados/meus_casos.csv"

# --------------------------------------------------------------------------
# Os limiares das regras — TODO: troque pelos do SEU domínio.
# (Os valores abaixo são os do domínio de exemplo: máquinas industriais.)
# --------------------------------------------------------------------------
LIMITE_POTENCIA_MIN = 3500.0       # W   — PWF
LIMITE_POTENCIA_MAX = 9000.0       # W   — PWF
LIMITE_DELTA_T = 8.6               # K   — HDF (com rpm baixo)
LIMITE_RPM_HDF = 1380              # rpm — HDF
LIMITE_OSF = {"L": 11000.0, "M": 12000.0, "H": 13000.0}   # desgaste*torque — OSF
DESGASTE_ATENCAO = 200             # min — TWF (troca/falha entre 200 e 240)
RISCO_ALTO = "alto"
RISCO_BAIXO = "baixo"
# --------------------------------------------------------------------------
# Estado interno — a memória do que o agente JÁ OBSERVOU do ambiente.
# O agente não sabe o futuro: ele acumula os desfechos que o ambiente
# revelou até agora. E "até agora" tem política de esquecimento — decidir
# por quanto tempo guardar é parte da decisão de estado interno (slide 24
# do E2). Sem a janela, duas falhas antigas deixariam a família inteira em
# inspeção para sempre. Quem apagar a segunda condição de decidir() pode
# apagar esta classe junto.
# --------------------------------------------------------------------------


class EstadoDaFrota:
    """O que o agente já observou: falhas por família, dentro da janela."""

    def __init__(self, janela_dias: int = JANELA_DIAS) -> None:
        self._janela = janela_dias
        self._falhas: list[tuple[str, _date]] = []
        self._ultima_data: _date | None = None

    def falhas_recentes(self, familia: str) -> int:
        """Quantas falhas desta família o agente viu, dentro da janela."""
        if self._ultima_data is None:
            return 0
        limite = self._ultima_data.toordinal() - self._janela
        return sum(
            1 for familia_vista, dia in self._falhas
            if familia_vista == familia and dia.toordinal() >= limite)

    def registrar_desfecho(self, registro: dict) -> None:
        """O ambiente revela o desfecho do caso — a percepção do próximo
        ciclo é maior do que a do anterior (parcialmente observável). Sem
        desfecho observado, não há o que registrar."""
        self._ultima_data = _date.fromisoformat(registro["data"])
        if int(registro.get("falhou_depois", 0)) == 1:
            self._falhas.append(
                (registro["tipo_maquina"], self._ultima_data))


# --------------------------------------------------------------------------
# A decisão — o coração do agente, em oito linhas (slide 22)
# --------------------------------------------------------------------------
def potencia(registro: dict) -> float:
    """Potência mecânica em watts: torque (Nm) x velocidade angular (rad/s)."""
    return registro["torque"] * registro["rotacao"] * 2 * math.pi / 60


def decidir(registro: dict) -> str:
    """Uma rodada: a leitura entra, o nível de risco sai.

    A primeira regra que casar decide — qualquer modo de falha provável
    basta para risco alto. A ordem das regras não muda o resultado, só
    qual delas é citada.
    """
    if registro["desgaste"] >= LIMITE_DESGASTE:
        return RISCO_ALTO
    delta_t = registro["temperatura_processo"] - registro["temperatura_ar"]
    if delta_t < LIMITE_DELTA_T and registro["rotacao"] < LIMITE_ROTACAO_HDF:
        return RISCO_ALTO
    if not POTENCIA_MINIMA <= potencia(registro) <= POTENCIA_MAXIMA:
        return RISCO_ALTO
    if registro["desgaste"] * registro["torque"] > LIMITE_SOBRECARGA[registro["tipo"]]:
        return RISCO_ALTO
    return RISCO_BAIXO

def carregar_casos(caminho: str | Path = CAMINHO_DOS_CASOS) -> list[dict]:
    """Lê o CSV de casos rotulados (colunas originais do AI4I) e converte os campos."""
    with Path(caminho).open(encoding="utf-8-sig", newline="") as arquivo:
        linhas = list(csv.DictReader(arquivo))
    casos = []
    for linha in linhas:
        caso = {chave: linha[coluna] for coluna, chave in COLUNAS.items()}
        caso.update(id_caso=linha["id_caso"], risco_correto=linha["risco_correto"],
                    categoria=linha["categoria"])
        caso["udi"] = int(caso["udi"])
        caso["temperatura_ar"] = float(caso["temperatura_ar"])
        caso["temperatura_processo"] = float(caso["temperatura_processo"])
        caso["rotacao"] = int(caso["rotacao"])
        caso["torque"] = float(caso["torque"])
        caso["desgaste"] = int(caso["desgaste"])
        caso["falha"] = int(caso["falha"])
        casos.append(caso)
    return casos


if __name__ == "__main__":
    from medir import medir_e_imprimir

    medir_e_imprimir(CAMINHO_DOS_CASOS, decidir, EstadoDaFrota)
