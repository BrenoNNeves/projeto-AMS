from __future__ import annotations

from ams.baseline import CAMINHO_DOS_CASOS, carregar_casos, decidir, medir

LEITURA_NORMAL = {
    "tipo": "M", "temperatura_ar": 298.1, "temperatura_processo": 308.6,
    "rotacao": 1551, "torque": 42.8, "desgaste": 0,
}


def leitura(**mudancas) -> dict:
    return {**LEITURA_NORMAL, **mudancas}


# --------------------------------------------------------------------------
# Regras do agente (uma por modo de falha)
# --------------------------------------------------------------------------
def test_leitura_normal_e_risco_baixo() -> None:
    assert decidir(leitura()) == "baixo"


def test_desgaste_no_limite_e_risco_alto() -> None:
    assert decidir(leitura(desgaste=200)) == "alto"
    assert decidir(leitura(desgaste=199)) == "baixo"


def test_delta_t_baixo_so_conta_com_rotacao_baixa() -> None:
    baixo_dt = {"temperatura_processo": 306.0}  # delta de 7,9 K
    assert decidir(leitura(rotacao=1300, **baixo_dt)) == "alto"
    assert decidir(leitura(rotacao=1500, **baixo_dt)) == "baixo"


def test_potencia_fora_da_faixa_e_risco_alto() -> None:
    assert decidir(leitura(torque=10.0, rotacao=2678)) == "alto"   # ~2.800 W
    assert decidir(leitura(torque=66.0, rotacao=1400)) == "alto"   # ~9.700 W


def test_sobrecarga_depende_do_tipo_de_produto() -> None:
    sobrecarga = {"desgaste": 190, "torque": 60.0, "rotacao": 1400}
    assert decidir(leitura(tipo="L", **sobrecarga)) == "alto"   # 11.400 > 11.000
    assert decidir(leitura(tipo="M", **sobrecarga)) == "baixo"  # 11.400 < 12.000


# --------------------------------------------------------------------------
# O conjunto de avaliação (30_novos_casos_ams.csv)
# --------------------------------------------------------------------------
def test_conjunto_tem_30_casos_com_atipicos() -> None:
    casos = carregar_casos(CAMINHO_DOS_CASOS)
    categorias = {c["categoria"] for c in casos}
    assert len(casos) == 30
    assert {"falha", "facil", "atipico"} <= categorias
    assert sum(c["categoria"] == "atipico" for c in casos) >= 2


def test_conjunto_tem_ids_unicos_e_rotulos_validos() -> None:
    casos = carregar_casos(CAMINHO_DOS_CASOS)
    assert len({c["id_caso"] for c in casos}) == 30
    assert len({c["udi"] for c in casos}) == 30
    assert {c["risco_correto"] for c in casos} <= {"alto", "baixo"}


def test_rotulo_do_risco_e_coerente_com_a_falha() -> None:
    for c in carregar_casos(CAMINHO_DOS_CASOS):
        esperado = "alto" if c["falha"] else "baixo"
        assert c["risco_correto"] == esperado, c["id_caso"]


def test_conjunto_distribuicao_por_categoria() -> None:
    casos = carregar_casos(CAMINHO_DOS_CASOS)
    contagem = {cat: sum(c["categoria"] == cat for c in casos)
                for cat in ("facil", "falha", "atipico")}
    assert contagem == {"facil": 10, "falha": 17, "atipico": 3}


# --------------------------------------------------------------------------
# A medição (valores do relatório: se o baseline mudar, estes testes avisam)
# --------------------------------------------------------------------------
def test_medicao_devolve_a_metrica_primaria() -> None:
    resultado = medir()
    assert resultado["total"] == 30
    assert resultado["com_falha"] + resultado["sem_falha"] == 30
    assert 0.0 <= resultado["taxa_antecipadas"] <= 1.0
    assert resultado["falhas_antecipadas"] <= resultado["com_falha"]
    assert resultado["com_falha"] == 20
    assert resultado["sem_falha"] == 10


def test_medicao_bate_com_o_relatorio() -> None:
    r = medir()
    assert (r["falhas_antecipadas"], r["com_falha"]) == (14, 20)
    assert r["taxa_antecipadas"] == 0.7
    assert r["alarmes_falsos"] == 0
    assert r["acertos"] == 24


def test_falhas_perdidas_sao_as_previstas() -> None:
    perdidas = {c["id_caso"] for c in medir()["falhas_perdidas"]}
    assert perdidas == {"C52", "C53", "C55", "C59", "C67", "C70"}


def test_falhas_aleatorias_sem_sinal_nao_sao_antecipadas() -> None:
    """Limitação conhecida: RNF sem rastro nos sensores escapa de qualquer limiar."""
    por_id = {c["id_caso"]: c for c in carregar_casos(CAMINHO_DOS_CASOS)}
    for id_caso in ("C55", "C67", "C70"):
        assert decidir(por_id[id_caso]) == "baixo", id_caso