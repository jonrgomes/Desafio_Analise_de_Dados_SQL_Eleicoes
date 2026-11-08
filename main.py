# Desafio Eleições 2026
import json

with open("eleicoes_2026.json", encoding="utf-8") as arquivo:
    base =  json.load(arquivo)
    
candidato = base["candidatos"]
disputa = base["disputas"]
print("\n-----DESAFIO ELEIÇÕES 2026(FAKE)------\n")
print('Nível 01 - LAÇOS DE REPETIÇÃO:\n')

print("1 - Dados da eleição 2026:\n")
candidatos = len(base["candidatos"])
disputa = len(base['disputas'])
ufs = len(base["ufs"])
partidos = len(base["partidos"])

print(f'Candidatos: {candidatos}')
print(f'Disputas: {disputa}')
print(f'UFS: {ufs}')
print(f'Partidos: {partidos}\n')

print("1 - 10 Primeiros candidatos:\n")
for dados1, dados2 in enumerate(candidato[0:10], 1):
    print(f"{dados1} - {dados2["nome_urna"]} | {dados2["cargo"]} | {dados2["uf"]} | {dados2["partido"]}")