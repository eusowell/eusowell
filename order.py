import os
import json

with open('data.json', 'r') as fp:
        data = json.load(fp)


lst_nomes = []
for d in data:
    lst_nomes.append(f'{d["id"]} - {d["primaryEmail"]} - {d["creationTime"]}')
    print(f'Id = {d["id"]} - Nome= {d["primaryEmail"]} data criação {d["creationTime"]}')


with open('listaiordenada.txt', 'w') as f:
        f.write("\n".join(sorted(lst_nomes)))

# print(sorted(lst_nomes))