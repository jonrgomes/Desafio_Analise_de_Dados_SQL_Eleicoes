# 🗳️ Desafio Python — Apuração Eleitoral 2026 (dados fictícios)

Você vai aprender Python analisando uma eleição inventada. Começa simples (laços e dicionários), depois usa **funções**, depois **classes com tipagem**, e termina com um programa completo.

**Regra de ouro:** faça um desafio por vez, na ordem. Cada um usa o que você aprendeu no anterior.

---

## 1. Arquivos

| Arquivo | O que é |
|---|---|
| `eleicoes_2026.json` | Os dados: 2000 candidatos, 109 disputas, 27 UFs, 12 partidos |
| `eleicoes_2026.db` | Os mesmos dados em banco SQLite (para o Beekeeper Studio) |
| `criar_banco.py` | Script que cria o `.db` a partir do JSON |
| `desafios_eleicoes.md` | Este guia |

## 2. Antes de começar

### 2.1 Abrir o arquivo (use isto no início de todo desafio)

```python
import json

with open("eleicoes_2026.json", encoding="utf-8") as arquivo:
    base = json.load(arquivo)

candidatos = base["candidatos"]   # lista com 2000 dicionários
disputas = base["disputas"]       # lista com 109 dicionários
```

### 2.2 Mini-guia: o que você vai usar

| Conceito | Exemplo |
|---|---|
| Laço `for` | `for c in candidatos:` |
| Condição `if` | `if c["uf"] == "SP":` |
| Dicionário | `c["nome_urna"]` ou `c.get("vice")` (o `.get` não dá erro se a chave não existir) |
| Lista nova | `lista = []` e `lista.append(c)` |
| Contador | `contagem[x] = contagem.get(x, 0) + 1` |
| Função | `def media(numeros): return sum(numeros) / len(numeros)` |
| Classe | `class Candidato:` (aparece no Nível 3) |
| Tipagem | `def dobro(x: int) -> int:` |

### 2.3 Regras

1. Python 3.10 ou mais novo. Só a biblioteca padrão (sem pandas).
2. Um arquivo por desafio: `desafio_01.py`, `desafio_02.py`…
3. **Não altere os dados originais.** Crie listas e dicionários novos.
4. Confira seu resultado no **gabarito** (final do guia), só depois de tentar.
5. Errou? Use `print()` para ver o que está dentro de cada variável.

---

## 3. Como os dados são organizados

```text
base
├── metadados      → regras e avisos
├── ufs            → 27 UFs
├── partidos       → 12 partidos (fictícios)
├── disputas       → 109 disputas (1 por cargo e UF)
└── candidatos     → 2000 candidatos
```

**Disputas:** `BR-PRE` (Presidente) e, para cada UF, `XX-GOV` (Governador), `XX-SEN` (Senador), `XX-DEF` (Deputado Federal) e `XX-DEE` (Deputado Estadual; no DF é `DF-DID`).

### 3.1 Campos do candidato

| Campo | O que é |
|---|---|
| `id` | Número único |
| `nome_completo`, `nome_urna` | Nomes |
| `numero_urna` | Número (texto, não inteiro) |
| `cargo`, `uf`, `id_disputa` | Onde ele disputa |
| `partido`, `federacao` | Partido (e federação, ou `None`) |
| `genero`, `cor_raca`, `estado_civil`, `grau_instrucao`, `ocupacao`, `idade` | Perfil |
| `reeleicao` | `True` se já tem mandato |
| `situacao_candidatura` | `Deferido` ou inapto (`Indeferido`, `Renúncia`, `Cancelado`) |
| `patrimonio_declarado` | Valor em R$ (pode ser `None`) |
| `vice` / `suplentes` | Só existem para alguns cargos |
| `campanha` | `receita_total`, `despesa_total` e `fontes_receita` |
| `apuracao` | Votos e resultado (veja abaixo) |

**Onde estão os votos e o resultado:**

```python
c["apuracao"]["turno1"]["votos_nominais"]      # votos do candidato
c["apuracao"]["turno1"]["colocacao"]           # 1º, 2º, 3º...
c["apuracao"]["situacao_totalizacao"]          # "Eleito", "Suplente", "Não eleito"...
```

`situacao_totalizacao` pode ser: `Eleito`, `Eleito por QP`, `Eleito por média`, `Suplente`, `Não eleito` ou `Candidatura inapta`. **Eleito é todo valor que começa com "Eleito".**

### 3.2 Campos da disputa

`id_disputa`, `cargo`, `uf`, `cadeiras` e `turno1` (com `eleitorado_apto`, `comparecimento`, `abstencoes`, `votos_brancos`, `votos_nulos`, `votos_validos`).

### 3.3 Regras da eleição (resumo)

- **Presidente e Governador:** ganha quem tem mais de 50% dos votos válidos. Se ninguém tem, vai para o 2º turno.
- **Senador:** 2 vagas, cada eleitor vota 2 vezes.
- **Deputados:** as vagas são divididas entre os partidos de acordo com os votos (sistema proporcional).
- **Votos válidos** = comparecimento − brancos − nulos.
- **Escala:** as cadeiras de deputado foram reduzidas (cadeiras reais ÷ 4, arredondando para cima) para a disputa ficar acirrada com 2000 candidatos. Total: **490 cadeiras**.

### 3.4 Sujeiras propositais nos dados

Patrimônio `None`, ocupação `"NÃO INFORMADO"`, `nome_urna` em MAIÚSCULAS ou com espaços a mais, candidatos inaptos (sem votos).

### 3.5 Exemplo de candidato

```json
{
  "id": 13,
  "nome_completo": "Karen Pacheco Sousa",
  "nome_urna": "Karen Pacheco",
  "numero_urna": "8365",
  "cargo": "Deputado Federal",
  "uf": "BA",
  "id_disputa": "BA-DEF",
  "partido": "MHZ",
  "federacao": "Federação Horizonte Verde",
  "genero": "Feminino",
  "cor_raca": "Branca",
  "data_nascimento": "1996-06-25",
  "idade": 30,
  "estado_civil": "Casado(a)",
  "grau_instrucao": "Pós-graduação",
  "ocupacao": "Advogado(a)",
  "reeleicao": false,
  "situacao_candidatura": "Deferido",
  "patrimonio_declarado": 382982.11,
  "campanha": {
    "receita_total": 1716561.68,
    "despesa_total": 1592812.3,
    "fontes_receita": {
      "fundo_eleitoral": 1126589.73,
      "fundo_partidario": 166933.82,
      "doacoes_pessoas_fisicas": 277386.61,
      "recursos_proprios": 145651.52
    }
  },
  "redes_sociais": {
    "seguidores_total": 15058,
    "plataformas": [
      "WhatsApp",
      "X"
    ]
  },
  "temas_prioritarios": [
    "Cultura",
    "Saúde",
    "Assistência Social"
  ],
  "historico_eleitoral": [],
  "apuracao": {
    "turno1": {
      "votos_nominais": 130776,
      "percentual_votos_validos": 1.4901,
      "colocacao": 12,
      "votos_por_area": {
        "capital": 20649,
        "regiao_metropolitana": 38608,
        "interior": 71519
      }
    },
    "turno2": null,
    "lista": "Federação Horizonte Verde",
    "posicao_na_lista": 3,
    "situacao_totalizacao": "Eleito por média"
  }
}
```

---

## 4. Os 20 desafios


### 🟢 Nível 1 — Laços e dicionários (sem funções)

#### Desafio 01 — Abrir e conhecer os dados
**Missão:** abrir o JSON e mostrar o tamanho de cada parte.
**Use:** `json.load`, `len`, `print`.
**Passos:**
1. Abra o arquivo (código da seção 2.1).
2. Imprima quantos candidatos, disputas, UFs e partidos existem.
3. Imprima as chaves do primeiro candidato: `print(candidatos[0].keys())`.

**Saída esperada:** `2000 candidatos`, `109 disputas`, `27 UFs`, `12 partidos`.

#### Desafio 02 — Percorrer a lista com `for`
**Missão:** mostrar os 10 primeiros candidatos.
**Use:** `for`, `enumerate`, f-string.
**Passos:**
1. Percorra `candidatos[:10]`.
2. Para cada um, imprima: `1 - Maria Souza | Deputado Federal | BA | ACV`.

**Dica:** `for i, c in enumerate(candidatos[:10], 1):`

#### Desafio 03 — Contar com dicionário
**Missão:** contar quantos candidatos existem em cada cargo.
**Use:** `for`, dicionário, `.get`.
**Passos:**
1. Crie `contagem = {}`.
2. Para cada candidato, faça `contagem[c["cargo"]] = contagem.get(c["cargo"], 0) + 1`.
3. Imprima cada cargo e o total.

**Saída esperada:** 6 cargos; a soma é 2000.
**Bônus:** repita para `partido` e `genero`.
**Bônus SQL (Beekeeper):** `SELECT cargo, COUNT(*) FROM candidatos GROUP BY cargo;`

#### Desafio 04 — Filtrar com `if`
**Missão:** achar os candidatos a Deputado Federal por São Paulo.
**Use:** `for`, `if`, `and`, `.append`.
**Passos:**
1. Crie `resultado = []`.
2. Para cada candidato, se `cargo == "Deputado Federal"` **e** `uf == "SP"`, adicione em `resultado`.
3. Imprima quantos foram encontrados e o `nome_urna` de cada um.

**Bônus:** liste só as mulheres do partido `ACV`.
**Bônus SQL:** `SELECT COUNT(*) FROM candidatos WHERE uf = 'SP' AND cargo = 'Deputado Federal';`

#### Desafio 05 — Somar, média, maior e menor
**Missão:** calcular números a partir de um laço.
**Use:** `for`, variáveis acumuladoras (`soma = 0`), `if` para guardar o maior.
**Passos:**
1. Calcule a **idade média** de todos os candidatos (soma ÷ quantidade).
2. Descubra o **candidato mais votado** a Deputado Federal em SP (guarde o maior valor e o nome).
3. Some os votos nominais do partido `ACV` para Deputado Federal.

**Dica:** comece com `maior = 0` e atualize com `if votos > maior:`.
**Bônus SQL:** `SELECT AVG(idade) FROM candidatos;`

---

### 🟡 Nível 2 — Funções

Agora você transforma seus laços em **funções** que podem ser reutilizadas.

#### Desafio 06 — Função de contagem
**Missão:** criar `contar_por(lista, campo)`.
**Use:** `def`, `return`, dicionário.
**Passos:**
1. A função recebe a lista de candidatos e o nome do campo (`"cargo"`, `"uf"`, `"partido"`...).
2. Devolve um dicionário com as contagens.
3. Teste com `cargo`, `uf`, `partido` e `genero`.

**Saída esperada:** o resultado de `contar_por(candidatos, "cargo")` é igual ao do Desafio 03.

#### Desafio 07 — Função de filtro
**Missão:** criar `filtrar(lista, cargo=None, uf=None, partido=None)`.
**Use:** parâmetros com valor padrão (`=None`), `if`.
**Passos:**
1. Percorra a lista.
2. Ignore o filtro que for `None`.
3. Devolva uma lista nova só com quem passou em **todos** os filtros informados.

**Teste:** `filtrar(candidatos, cargo="Deputado Federal", uf="SP")` deve dar o mesmo resultado do Desafio 04.
**Dica:** use `continue` quando o candidato não passar em um filtro.

#### Desafio 08 — Buscar por nome
**Missão:** criar `buscar_nome(lista, texto)`.
**Use:** `.lower()`, `in`, `unicodedata`.
**Passos:**
1. Procure o texto em `nome_urna` e `nome_completo`.
2. Ignore maiúsculas e minúsculas.
3. Ignore acentos (`José` = `jose`).

**Dica:**
```python
import unicodedata
def sem_acento(texto):
    return "".join(ch for ch in unicodedata.normalize("NFD", texto) if unicodedata.category(ch) != "Mn")
```

#### Desafio 09 — Ranking dos mais votados
**Missão:** criar `top_n(lista, id_disputa, n)`.
**Use:** `sorted`, `key`, `lambda`, fatiamento `[:n]`.
**Passos:**
1. Filtre os candidatos da disputa.
2. Ordene do mais para o menos votado.
3. Devolva os `n` primeiros.

**Saída esperada:** `top_n(candidatos, "BR-PRE", 3)` mostra os 3 do gabarito.
**Dica:** `sorted(lista, key=lambda c: c["apuracao"]["turno1"]["votos_nominais"], reverse=True)`
**Bônus SQL:** `SELECT nome_urna, t1_votos_nominais FROM candidatos WHERE id_disputa = 'BR-PRE' ORDER BY t1_votos_nominais DESC LIMIT 3;`

#### Desafio 10 — Eleitos × não eleitos
**Missão:** criar `media(lista, campo)` e `percentual(parte, total)` e usá-las para comparar os grupos.
**Use:** funções que chamam outras funções, `startswith`.
**Passos:**
1. Separe `eleitos` (situação começa com `"Eleito"`) e `nao_eleitos` (o resto, sem os inaptos).
2. Calcule: idade média de cada grupo e % de mulheres entre os eleitos.
3. Imprima uma tabelinha com os resultados.

**Cuidado:** se a lista estiver vazia, a divisão dá erro. Trate esse caso.

---

### 🟠 Nível 3 — Classes e tipagem

Agora os dados deixam de ser "dicionários soltos" e viram **objetos** com tipos definidos.

#### Desafio 11 — Sua primeira classe
**Missão:** criar a classe `Candidato` com `@dataclass`.
**Use:** `dataclass`, tipagem de campos (`str`, `int`, `float`, `bool`).
**Passos:**
1. Crie a classe com: `id`, `nome_urna`, `cargo`, `uf`, `partido`, `idade`, `genero`, `votos`, `situacao`.
2. Crie a função `criar_candidato(dados: dict) -> Candidato` que lê o dicionário do JSON.
3. Converta os 2000 candidatos para uma lista de objetos.
4. Imprima um deles: `print(objetos[0])`.

**Modelo:**
```python
from dataclasses import dataclass

@dataclass
class Candidato:
    id: int
    nome_urna: str
    cargo: str
    # ... complete os outros campos
```

#### Desafio 12 — Métodos na classe
**Missão:** colocar comportamento dentro do `Candidato`.
**Use:** métodos (`def nome(self)`), `-> bool`, `-> float`, `-> str`.
**Passos:** adicione à classe:
1. `foi_eleito(self) -> bool`
2. `faixa_etaria(self) -> str` (`"18-29"`, `"30-39"`, `"40-49"`, `"50-59"`, `"60+"`)
3. `custo_por_voto(self) -> float` (despesa ÷ votos; devolva `0.0` se não houve votos). Para isso, inclua `despesa` e `receita` na classe.

**Bônus:** calcule o custo por voto médio dos eleitos a Deputado Federal.

#### Desafio 13 — A classe Disputa
**Missão:** criar a classe `Disputa`, que guarda os candidatos dela.
**Use:** classe com `__init__` ou `dataclass`, lista de objetos dentro de objeto.
**Passos:** a `Disputa` tem `id_disputa`, `cargo`, `uf`, `cadeiras`, `votos_validos` e `candidatos: list[Candidato]`. Crie os métodos:
1. `total_votos(self) -> int` — soma dos votos dos candidatos
2. `vencedores(self) -> list[Candidato]` — quem foi eleito
3. `margem(self) -> float` — diferença de votos (em %) entre o 1º e o 2º (use `votos_validos`)

**Teste:** monte a disputa `SP-DEF` e confira o gabarito.

#### Desafio 14 — A classe BaseEleitoral
**Missão:** juntar tudo em uma classe que carrega e consulta os dados.
**Use:** `__init__`, métodos, dicionário de disputas, tipagem `list[Candidato]`, `Optional`.
**Passos:**
1. `__init__(self, caminho: str)` carrega o JSON e cria as listas de `Candidato` e `Disputa`.
2. `buscar(self, cargo=None, uf=None, partido=None, texto=None) -> list[Candidato]` (reaproveite as ideias dos Desafios 7 e 8).
3. `disputa(self, id_disputa: str) -> Optional[Disputa]`
4. `contar_por(self, campo: str) -> dict[str, int]`

**Uso esperado:**
```python
base = BaseEleitoral("eleicoes_2026.json")
print(len(base.buscar(cargo="Deputado Federal", uf="SP")))
print(base.disputa("SP-DEF").total_votos())
```

#### Desafio 15 — Testes simples
**Missão:** provar que seu código funciona.
**Use:** `unittest`, `assert`.
**Passos:** crie `teste_base.py` com pelo menos 5 testes, por exemplo:
1. a base tem 2000 candidatos;
2. `foi_eleito()` é `True` para um eleito e `False` para um suplente;
3. `faixa_etaria()` devolve `"60+"` para 65 anos;
4. `buscar(texto="jose")` encontra nomes com acento;
5. `disputa("XX")` devolve `None`.

**Rode com:** `python -m unittest`

---

### 🔴 Nível 4 — Apuração eleitoral

Aqui você usa tudo para calcular as métricas de uma apuração.

#### Desafio 16 — Juntar candidato, disputa e partido
**Missão:** mostrar, para cada candidato, os dados da disputa e do partido dele.
**Use:** dicionários de consulta (índice), laço, `BaseEleitoral`.
**Passos:**
1. Crie `indice_disputas = {d["id_disputa"]: d for d in disputas}` e um índice de partidos pela `sigla`.
2. Para o 1º colocado a Presidente, imprima: nome, partido, **espectro do partido**, eleitorado da disputa e **% do eleitorado** que votou nele (votos ÷ eleitorado apto).
3. Verifique se existe algum candidato cujo `id_disputa`, `partido` ou `uf` não existe nos índices (deve dar **zero**).

**Dica:** o índice evita um `for` dentro de outro `for`.

#### Desafio 17 — Métricas da apuração
**Missão:** calcular comparecimento, abstenção, brancos e nulos de uma disputa.
**Use:** funções, f-string com `:.2f`.
**Passos:** crie `resumo_apuracao(disputa) -> dict` que devolve:
1. comparecimento % (comparecimento ÷ eleitorado apto);
2. abstenção % (100 − comparecimento %);
3. brancos % e nulos % (sobre o comparecimento).

Depois, para **todas** as disputas, confira: a soma dos votos dos candidatos é igual a `votos_validos`? (Nas disputas de Deputado, falta somar os votos de legenda: `turno1["votos_legenda"]`. No Senado cada eleitor tem 2 votos.)

**Teste:** `SP-DEF` deve bater com o gabarito.
**Bônus SQL:** `SELECT id_disputa, ROUND(100.0 * t1_comparecimento / t1_eleitorado_apto, 2) AS comparecimento_pct FROM disputas WHERE id_disputa = 'SP-DEF';`

#### Desafio 18 — Disputas acirradas
**Missão:** descobrir onde a eleição foi mais apertada.
**Use:** laço, `sorted`, métodos da classe `Disputa`.
**Passos:**
1. Para cada disputa de **Governador**, calcule a margem entre o 1º e o 2º (em pontos percentuais).
2. Liste as 5 mais apertadas.
3. Para **Deputado Federal**, calcule candidatos por cadeira em cada UF e mostre as 5 UFs mais concorridas.

**Teste:** a mais apertada deve bater com o gabarito.
**Bônus:** calcule o **número efetivo de candidatos**: `1 / soma(p²)`, onde `p` é a fração de votos de cada candidato (`percentual_votos_validos / 100`). Teste com o Presidente.

#### Desafio 19 — A eleição para Presidente
**Missão:** reconstruir o resultado nacional.
**Use:** laço dentro de laço, dicionário dentro de dicionário.
**Passos:**
1. Para cada candidato a Presidente, some os valores de `c["apuracao"]["turno1"]["votos_por_uf"]`. O total deve ser igual a `votos_nominais`.
2. Calcule o % de cada um sobre os votos válidos nacionais.
3. Houve 2º turno? (Alguém passou de 50%?)
4. Descubra **quem venceu em cada UF** e quantas UFs cada candidato ganhou.

**Teste:** compare com o gabarito.

#### Desafio 20 — Projeto final: menu no terminal
**Missão:** criar um programa com menu usando tudo que aprendeu.
**Use:** `while True`, `input`, `BaseEleitoral`, funções, `csv` ou `json` para salvar.
**Passos:** o programa mostra:
```text
1 - Resumo da eleição
2 - Buscar candidato por nome
3 - Ranking de uma disputa
4 - Métricas de uma disputa
5 - Salvar relatório (CSV)
0 - Sair
```
Cada opção chama um método ou função que você já fez. Opção 0 encerra o `while`. Trate entradas inválidas (ex.: disputa que não existe).

**Critério:** o programa roda do início ao fim sem erro e o relatório CSV abre no Excel.

---

## 5. Depois dos 20 (desafios extras)

Quando terminar, tente:
1. **Quociente eleitoral:** recalcule `votos_validos ÷ cadeiras` de cada disputa de Deputado e compare com `turno1["quociente_eleitoral"]`.
2. **Sobras (maior média):** refaça a divisão de cadeiras entre as listas e compare com `disputas[].listas`.
3. **Motor de busca rápido:** monte índices (`dict` de nome → candidatos) e compare o tempo com a busca por `for`.

---

## 6. Checklist de cada desafio

- [ ] Roda sem erro
- [ ] O resultado bate com o gabarito
- [ ] Os nomes de variáveis e funções são claros
- [ ] Não alterei os dados originais
- [ ] Usei tipagem e comentários onde ajudou (a partir do Nível 3)

---

## 7. Gabarito de conferência

<details>
<summary><b>Clique somente depois de tentar!</b></summary>

| Desafio | Valor esperado |
|---|---|
| 01 | 2000 candidatos · 109 disputas · 27 UFs · 12 partidos |
| 03 | Candidatos por cargo: Presidente 8 · Governador 104 · Senador 111 · Dep. Federal 605 · Dep. Estadual 1148 · Dep. Distrital 24 |
| 04 | Dep. Federal por SP: **80** candidatos · candidatos do partido ACV (todos os cargos): **204** |
| 05 | Idade média de todos os candidatos: **48,32** · mais votado a Dep. Federal em SP: **Paulo Ferreira** (8.135.486 votos) · votos do ACV a Dep. Federal: **12.741.511** |
| 09 | Presidente — Top 3 no 1º turno:<br>1. Marcelo Sousa (FRN) — 31.677.889 votos (26,3987%)<br>2. Heitor Sousa (EQP) — 15.584.097 votos (12,9870%)<br>3. Guilherme Viana (BRV) — 14.629.843 votos (12,1917%) |
| 10 | Idade média dos eleitos (todos os cargos): **48,25** · mulheres entre os eleitos: **32,86%** |
| 12 | Custo por voto médio dos eleitos a Dep. Federal: **R$ 4,21** |
| 13 | `SP-DEF`: **18** cadeiras · **80** candidatos · 4,44 candidatos por cadeira |
| 16 | 1º colocado a Presidente: **Marcelo Sousa** com **19,89%** do eleitorado apto (159.300.000) · órfãos: 0 |
| 17 | `SP-DEF`: comparecimento **76,31%** · abstenção **23,69%** · brancos **3,69%** · nulos **5,13%** (sobre o comparecimento) |
| 18 | Governador mais apertado: **AM-GOV** (1,8610 p.p.) · governadores com 2º turno: **18** de 27 · bônus (nº efetivo de candidatos do Presidente): **6,607** |
| 19 | Votos válidos nacionais: **119.997.958** · 2º turno: **sim** · eleito: **Marcelo Sousa** · UFs vencidas pelo líder do 1º turno: **27** |
| Extra 1 | Quociente eleitoral de `SP-DEF`: **1.387.627** |
| Extra 2 | Cadeiras por quociente partidário: **265** · por média: **143** · total: 408 |

**Cadeiras em disputa × candidatos × eleitos**

| Cargo | Candidatos | Cadeiras | Eleitos |
|---|---|---|---|
| Presidente | 8 | 1 | 1 |
| Governador | 104 | 27 | 27 |
| Senador | 111 | 54 | 54 |
| Deputado Federal | 605 | 136 | 136 |
| Deputado Estadual | 1.148 | 266 | 266 |
| Deputado Distrital | 24 | 6 | 6 |

**`situacao_totalizacao`:** Suplente 793 · Não eleito 673 · Eleito por QP 265 · Eleito por média 143 · Eleito (majoritário) 82 · Candidatura inapta 44

**Sujeiras nos dados:** patrimônio `None`: 60 · ocupação "NÃO INFORMADO": 40 · `nome_urna` com MAIÚSCULAS ou espaços extras: 40 · candidatos inaptos: 44

</details>

---

*Bons estudos! Travou? Me envie seu código e a mensagem de erro que eu te ajudo a entender o que aconteceu.* 🐍
