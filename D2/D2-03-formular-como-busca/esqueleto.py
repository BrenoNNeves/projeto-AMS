"""Laboratório 03 — reunir evidências para avaliar uma ordem de manutenção.

O subproblema é decidir quais fontes consultar para reunir os dados
necessários à avaliação de uma ordem de serviço do AMS. A classificação de
risco e as recomendações de segurança ficam fora desta formulação: o objetivo
da busca é obter as evidências de que essas etapas precisam.

Os dados abaixo descrevem um caso didático. Rode este arquivo para conferir
as seis verificações:

    python esqueleto.py
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Fonte:
    """Uma fonte consultável e as evidências que ela retorna."""

    nome: str
    latencia: float
    fornece: tuple[str, ...]


FATOS_NECESSARIOS: frozenset[str] = frozenset({
    "identificação e tipo da máquina",
    "leituras atuais de temperatura, rotação, torque e desgaste",
    "referência de falhas para avaliar as leituras",
    "descrição e escopo da ordem de serviço",
    "fontes de energia e pontos de isolamento da máquina",
    "condições da intervenção: atividade elétrica e trabalho em altura",
    "critérios das NR-10, NR-12, NR-35 e de bloqueio LOTO",
})

FONTES: tuple[Fonte, ...] = (
    Fonte(
        "sistema de ordens de serviço",
        0.8,
        (
            "identificação e tipo da máquina",
            "descrição e escopo da ordem de serviço",
            "condições da intervenção: atividade elétrica e trabalho em altura",
        ),
    ),
    Fonte(
        "gateway de sensores",
        1.2,
        ("leituras atuais de temperatura, rotação, torque e desgaste",),
    ),
    Fonte(
        "dataset AI4I 2020 de manutenção preditiva",
        2.0,
        ("referência de falhas para avaliar as leituras",),
    ),
    Fonte(
        "ficha técnica da máquina",
        2.5,
        (
            "identificação e tipo da máquina",
            "fontes de energia e pontos de isolamento da máquina",
        ),
    ),
    Fonte(
        "corpus documental das normas regulamentares",
        4.0,
        ("critérios das NR-10, NR-12, NR-35 e de bloqueio LOTO",),
    ),
    Fonte(
        "dossiê integrado da ordem de serviço",
        12.0,
        tuple(sorted(FATOS_NECESSARIOS)),
    ),
)


class MeuProblema:
    """Busca o conjunto de fontes que fornece as evidências necessárias.

    Estado inicial: nenhuma evidência consultada.
    Ações: consultar qualquer uma das fontes disponíveis.
    Transição: acrescentar ao estado os fatos retornados pela fonte.
    Objetivo: ter todos os fatos necessários para avaliar a ordem de serviço.
    Custo: latência da consulta, em segundos.

    O estado guarda o conjunto ordenado de fatos conhecidos, não a sequência
    de consultas que os encontrou; assim, caminhos diferentes para a mesma
    situação produzem o mesmo estado.
    """

    def __init__(self) -> None:
        self.fontes = FONTES
        self._por_nome = {fonte.nome: fonte for fonte in self.fontes}
        self.estado_inicial: tuple[str, ...] = ()

    def acoes(self, estado: tuple[str, ...]) -> list[str]:
        return [fonte.nome for fonte in self.fontes]

    def transicao(self, estado: tuple[str, ...], acao: str) -> tuple[str, ...]:
        return tuple(sorted(set(estado) | set(self._por_nome[acao].fornece)))

    def objetivo(self, estado: tuple[str, ...]) -> bool:
        return FATOS_NECESSARIOS.issubset(estado)

    def custo(
        self, estado: tuple[str, ...], acao: str, estado_seguinte: tuple[str, ...],
    ) -> float:
        return self._por_nome[acao].latencia


MEU_PROBLEMA = MeuProblema()


if __name__ == "__main__":
    import importlib.util
    import sys
    from pathlib import Path

    teste = importlib.util.spec_from_file_location(
        "verificar-formulacao",
        Path(__file__).resolve().parent / "verificar-formulacao.py")
    modulo = importlib.util.module_from_spec(teste)
    sys.modules["verificar-formulacao"] = modulo
    teste.loader.exec_module(modulo)
    raise SystemExit(modulo.main([str(Path(__file__)) + ":MEU_PROBLEMA"]))
