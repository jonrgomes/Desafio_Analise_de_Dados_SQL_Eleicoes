# Desafio Eleições 2026
import json

with open("eleicoes_2026.json", encoding="utf-8") as arquivo:
    base =  json.load(arquivo)
    
candidato = base["candidatos"]
disputa = base["disputas"]
print("\n-----DESAFIO ELEIÇÕES 2026(FAKE)------\n")
print('Nível 01 - laços e repetições:\n')

print("1 - DADOS DA ELEIÇÃO 2026:\n")
candidatos = len(base["candidatos"])
disputa = len(base['disputas'])
ufs = len(base["ufs"])
partidos = len(base["partidos"])

print(f'Candidatos: {candidatos}')
print(f'Disputas: {disputa}')
print(f'UFS: {ufs}')
print(f'Partidos: {partidos}')
