# Desafio Eleições 2026
import json

with open("eleicoes_2026.json", encoding="utf-8") as arquivo:
    base =  json.load(arquivo)
    
candidato = base["candidatos"]
disputa = base["disputas"]
print("\n-----DESAFIO ELEIÇÕES 2026(FAKE)------\n")
print('Nível 01 - LAÇOS DE REPETIÇÃO:\n')

print("----Dados da eleição 2026----\n")
candidatos = len(base["candidatos"])
disputa = len(base['disputas'])
ufs = len(base["ufs"])
partidos = len(base["partidos"])

print(f'Candidatos: {candidatos}')
print(f'Disputas: {disputa}')
print(f'UFS: {ufs}')
print(f'Partidos: {partidos}\n')

print("----10 Primeiros candidatos----\n")
for dados1, dados2 in enumerate(candidato[0:10], 1):
    print(f"{dados1} - {dados2["nome_urna"]} | {dados2["cargo"]} | {dados2["uf"]} | {dados2["partido"]}\n")

print("----Número de Candidatos por Cargo----\n")
contagem = {}
for qtd_candidatoscargo in candidato:
    cargo = qtd_candidatoscargo["cargo"]
    contagem[cargo] = contagem.get(cargo, 0) + 1
    
soma = 0
for cargo, total in contagem.items():
    print(f"{cargo}: {total}")
    soma += total

print(f"Soma: {soma}\n")

print("----Candidatos à Deputado Federal SP----\n")
dep_federal_sp = []
for cargo in candidato:
    if cargo["cargo"] == "Deputado Federal" and cargo["uf"] == "SP":
        dep_federal_sp.append(cargo)
print(f"Quantidade: {len(dep_federal_sp)}")

for cargo in dep_federal_sp:
    print(cargo["nome_urna"])
    
print("\n----Idade média dos candidatos-----\n")
maior = 0
for idade in candidato: 
    soma += idade["idade"]
    
media = soma / len(candidato)
print(f"Idade média: {media:.2f}.") 
maior = 0  
for votado in candidato: 
    votos = votado["apuracao"]["turno1"]["votos_nominais"]
    if votos > maior:
        maior = votos
print(f"Candiato mais votado: {maior}\n")

    

    
    
    
    