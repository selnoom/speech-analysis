import os 
import sys
from cProfile import label
from os.path import join
from praatio import textgrid

# python myscript.py > myoutput.txt
# Pasta com TextGrids
# dir_path = r'arquivos/NTB'
dir_path = sys.argv[1]

arquivosLista = []

for path in os.listdir(dir_path):
    if os.path.isfile(os.path.join(dir_path, path)):
        arquivosLista.append(path)
print(f'{arquivosLista}\n')

def Average(list):
    return sum(list) / len(list)

for arquivo in arquivosLista:
    inputFN = join(dir_path, arquivo)
    print(f'Arquivo: {inputFN}')

    tg = textgrid.openTextgrid(inputFN, includeEmptyIntervals=False) 

    print(f'Tiers: {tg.tierNameList}')

    tierList = []
    for tier in tg.tierNameList:
        # Remover comentários dos textgrids
        if tier != 'com':
            tierList.append(tg.tierDict[tier])

    durationList = []
    pausaList = []

    for tierDict in tierList:
        for start, stop, label in tierDict.entryList:
            if '...' not in label:
                durationList.append(stop - start)
            elif label == '...':
                pausaList.append(stop - start)

    segmentoMaximo = max(durationList)
    segmentoMinimo = min(durationList)
    segmentoMedia = Average(durationList)
    print(f'Tempo médio dos segmentos: {segmentoMedia}')
    print(f'Tempo máximo dos segmentos: {segmentoMaximo}')
    print(f'Tempo mínimo dos segmentos: {segmentoMinimo}\n')

    pausaMax = max(pausaList)
    pausaMin = min(pausaList)
    pausaMedia = Average(pausaList)
    print(f'Tempo médio das pausas: {pausaMedia}')
    print(f'Tempo máximo das pausas: {pausaMax}')
    print(f'Tempo mínimo das pausas: {pausaMin}\n')
    print('------------------------------------------\n')
