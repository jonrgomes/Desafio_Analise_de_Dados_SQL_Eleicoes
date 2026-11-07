"""Converte eleicoes_2026.json em eleicoes_2026.db (SQLite), pronto para o Beekeeper Studio

Uso:  python criar_banco.py [eleicoes_2026.json] [eleicoes_2026.db]
"""
import json
import sqlite3
import sys
from pathlib import Path

JSON_PATH = Path(sys.argv[1] if len(sys.argv) > 1 else "eleicoes_2026.json")
DB_PATH = Path(sys.argv[2] if len(sys.argv) > 2 else "eleicoes_2026.db")

SCHEMA = """
PRAGMA foreign_keys = ON;

CREATE TABLE ufs (
    sigla TEXT PRIMARY KEY, nome TEXT NOT NULL, regiao TEXT NOT NULL,
    eleitorado_apto INTEGER, cadeiras_reais_camara INTEGER, cadeiras_reais_assembleia INTEGER
);
CREATE TABLE partidos (
    sigla TEXT PRIMARY KEY, nome TEXT NOT NULL, numero INTEGER, espectro TEXT, federacao TEXT
);
CREATE TABLE disputas (
    id_disputa TEXT PRIMARY KEY, cargo TEXT NOT NULL, uf TEXT, circunscricao TEXT,
    cadeiras INTEGER, cadeiras_reais_referencia INTEGER, votos_por_eleitor INTEGER,
    total_candidatos INTEGER, houve_segundo_turno INTEGER, cadeiras_vagas INTEGER,
    secoes_totais INTEGER, secoes_totalizadas INTEGER,
    t1_eleitorado_apto INTEGER, t1_comparecimento INTEGER, t1_abstencoes INTEGER,
    t1_votos_brancos INTEGER, t1_votos_nulos INTEGER, t1_votos_validos INTEGER,
    t1_votos_nominais INTEGER, t1_votos_legenda INTEGER, quociente_eleitoral INTEGER,
    t2_eleitorado_apto INTEGER, t2_comparecimento INTEGER, t2_abstencoes INTEGER,
    t2_votos_brancos INTEGER, t2_votos_nulos INTEGER, t2_votos_validos INTEGER
);
CREATE TABLE listas_disputa (
    id_disputa TEXT NOT NULL REFERENCES disputas(id_disputa), lista TEXT NOT NULL, membros TEXT,
    votos_nominais INTEGER, votos_legenda INTEGER, votos_totais INTEGER, quociente_partidario INTEGER,
    candidatos_aptos_10pct_qe INTEGER, cadeiras_qp INTEGER, cadeiras_media INTEGER, cadeiras_total INTEGER,
    PRIMARY KEY (id_disputa, lista)
);
CREATE TABLE candidatos (
    id INTEGER PRIMARY KEY, nome_completo TEXT, nome_urna TEXT, numero_urna TEXT,
    cargo TEXT, uf TEXT, id_disputa TEXT NOT NULL REFERENCES disputas(id_disputa),
    partido TEXT NOT NULL REFERENCES partidos(sigla), federacao TEXT,
    genero TEXT, cor_raca TEXT, data_nascimento TEXT, idade INTEGER, estado_civil TEXT,
    grau_instrucao TEXT, ocupacao TEXT, reeleicao INTEGER, situacao_candidatura TEXT,
    patrimonio_declarado REAL, vice TEXT,
    receita_total REAL, despesa_total REAL, fundo_eleitoral REAL, fundo_partidario REAL,
    doacoes_pessoas_fisicas REAL, recursos_proprios REAL,
    seguidores_total INTEGER, plataformas TEXT,
    t1_votos_nominais INTEGER, t1_percentual REAL, t1_colocacao INTEGER,
    t2_votos_nominais INTEGER, t2_percentual REAL, t2_colocacao INTEGER,
    lista TEXT, posicao_na_lista INTEGER, situacao_totalizacao TEXT
);
CREATE TABLE candidato_temas (candidato_id INTEGER REFERENCES candidatos(id), tema TEXT);
CREATE TABLE candidato_suplentes (candidato_id INTEGER REFERENCES candidatos(id), ordem INTEGER, nome TEXT);
CREATE TABLE candidato_historico (candidato_id INTEGER REFERENCES candidatos(id), ano INTEGER, cargo TEXT, uf TEXT, resultado TEXT);
CREATE TABLE candidato_votos_uf (candidato_id INTEGER REFERENCES candidatos(id), turno INTEGER, uf TEXT, votos INTEGER);
CREATE TABLE candidato_votos_area (candidato_id INTEGER REFERENCES candidatos(id), area TEXT, votos INTEGER);

CREATE INDEX idx_cand_disputa ON candidatos(id_disputa);
CREATE INDEX idx_cand_partido ON candidatos(partido);
CREATE INDEX idx_cand_cargo_uf ON candidatos(cargo, uf);
CREATE INDEX idx_cand_situacao ON candidatos(situacao_totalizacao);
CREATE INDEX idx_votos_uf ON candidato_votos_uf(candidato_id);

CREATE VIEW v_eleitos AS
SELECT * FROM candidatos WHERE situacao_totalizacao LIKE 'Eleito%';
"""


def main() -> None:
    dados = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    DB_PATH.unlink(missing_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.executescript(SCHEMA)
    cur = con.cursor()

    cur.executemany("INSERT INTO ufs VALUES (?,?,?,?,?,?)",
                    [(u["sigla"], u["nome"], u["regiao"], u["eleitorado_apto"], u["cadeiras_reais_camara"],
                      u["cadeiras_reais_assembleia"]) for u in dados["ufs"]])
    cur.executemany("INSERT INTO partidos VALUES (?,?,?,?,?)",
                    [(p["sigla"], p["nome"], p["numero"], p["espectro"], p["federacao"]) for p in dados["partidos"]])

    for d in dados["disputas"]:
        t1, t2 = d["turno1"], d["turno2"] or {}
        cur.execute("INSERT INTO disputas VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
            d["id_disputa"], d["cargo"], d["uf"], d["circunscricao"], d["cadeiras"], d["cadeiras_reais_referencia"],
            d["votos_por_eleitor"], d["total_candidatos"], int(d["houve_segundo_turno"]), d.get("cadeiras_vagas"),
            d["secoes_totais"], d["secoes_totalizadas"],
            t1["eleitorado_apto"], t1["comparecimento"], t1["abstencoes"], t1["votos_brancos"], t1["votos_nulos"],
            t1["votos_validos"], t1.get("votos_nominais"), t1.get("votos_legenda"), t1.get("quociente_eleitoral"),
            t2.get("eleitorado_apto"), t2.get("comparecimento"), t2.get("abstencoes"), t2.get("votos_brancos"),
            t2.get("votos_nulos"), t2.get("votos_validos")))
        for l in d.get("listas", []):
            cur.execute("INSERT INTO listas_disputa VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                d["id_disputa"], l["lista"], ",".join(l["membros"]), l["votos_nominais"], l["votos_legenda"],
                l["votos_totais"], l["quociente_partidario"], l["candidatos_aptos_10pct_qe"],
                l["cadeiras_qp"], l["cadeiras_media"], l["cadeiras_total"]))

    for c in dados["candidatos"]:
        ap, camp = c["apuracao"], c["campanha"]
        t1, t2 = ap["turno1"], ap["turno2"] or {}
        f = camp["fontes_receita"]
        cur.execute("INSERT INTO candidatos VALUES (" + ",".join("?" * 37) + ")", (
            c["id"], c["nome_completo"], c["nome_urna"], c["numero_urna"], c["cargo"], c["uf"], c["id_disputa"],
            c["partido"], c["federacao"], c["genero"], c["cor_raca"], c["data_nascimento"], c["idade"],
            c["estado_civil"], c["grau_instrucao"], c["ocupacao"], int(c["reeleicao"]), c["situacao_candidatura"],
            c["patrimonio_declarado"], c.get("vice"),
            camp["receita_total"], camp["despesa_total"], f["fundo_eleitoral"], f["fundo_partidario"],
            f["doacoes_pessoas_fisicas"], f["recursos_proprios"],
            c["redes_sociais"]["seguidores_total"], ",".join(c["redes_sociais"]["plataformas"]),
            t1["votos_nominais"], t1["percentual_votos_validos"], t1["colocacao"],
            t2.get("votos_nominais"), t2.get("percentual_votos_validos"), t2.get("colocacao"),
            ap.get("lista"), ap.get("posicao_na_lista"), ap["situacao_totalizacao"]))
        cur.executemany("INSERT INTO candidato_temas VALUES (?,?)", [(c["id"], t) for t in c["temas_prioritarios"]])
        cur.executemany("INSERT INTO candidato_suplentes VALUES (?,?,?)",
                        [(c["id"], i, n) for i, n in enumerate(c.get("suplentes", []), 1)])
        cur.executemany("INSERT INTO candidato_historico VALUES (?,?,?,?,?)",
                        [(c["id"], h["ano"], h["cargo"], h["uf"], h["resultado"]) for h in c["historico_eleitoral"]])
        for turno, t in ((1, t1), (2, t2)):
            for uf, v in t.get("votos_por_uf", {}).items():
                cur.execute("INSERT INTO candidato_votos_uf VALUES (?,?,?,?)", (c["id"], turno, uf, v))
        for area, v in t1.get("votos_por_area", {}).items():
            cur.execute("INSERT INTO candidato_votos_area VALUES (?,?,?)", (c["id"], area, v))

    con.commit()
    for t in ("ufs", "partidos", "disputas", "listas_disputa", "candidatos", "candidato_votos_uf", "candidato_votos_area"):
        print(t, con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
    con.close()


if __name__ == "__main__":
    main()
