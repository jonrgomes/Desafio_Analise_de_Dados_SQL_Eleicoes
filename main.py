# Desafio Eleições 2026
import json

with open("eleicoes_2026.json", encoding="utf-8") as arquivo:
    base =  json.load(arquivo)

print('\n---TESTES INICIAIS DE AQUECIMENTO----\n')


candidatos = base['candidatos']
candidatos_eleitos = {}
for eleitos in candidatos[0:20]:
    print(eleitos['nome_urna'])

ufs = base["ufs"]
estados = 0
for uf in ufs:
    if uf["regiao"] == "Nordeste":
        estados += 1
print(f"Estados da região Nordeste: {estados}.")

    