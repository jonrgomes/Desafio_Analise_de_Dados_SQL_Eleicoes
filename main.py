# Desafio Eleições 2026
import json

with open("eleicoes_2026.json", encoding="utf-8") as arquivo:
    base =  json.load(arquivo)
    
candidato = base["candidato"]
disputa = base["disputa"]
print("\n-----DESAFIO ELEIÇÕES 2026(FAKE)------\n")
