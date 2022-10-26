import os
import re 
import sys
from cProfile import label
from os.path import join
from praatio import textgrid
from listas.pausasPreenchidas import PausasPreenchidas

# python myscript.py > myoutput.txt

# Pasta com TextGrids
dir_path = r'/home/nicholasp/Documentos/tcc/git/speech-analysis/analisador-textgrids/arquivos/TB'
# dir_path = sys.argv[1]

arquivosLista = []
pausasPreenchidas = [item.name for item in PausasPreenchidas]
durationListTotal = []
pausaListTotal = []
palavrasListTotal= []

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
    # Remove layer de comentários
    if 'com' in tg.tierNameList:
        tg.tierNameList.remove('com')
    
    print(f'Tiers: {tg.tierNameList}')

    tierList = []
    for tier in tg.tierNameList:
        tierList.append(tg.tierDict[tier])

    durationList = []
    pausaList = []
    palavrasList = []

    for tierDict in tierList:
        for start, stop, label in tierDict.entryList:
            if '...' not in label and label not in pausasPreenchidas:
                durationList.append(stop - start)
                if (re.search('[a-zA-Z]', label)):
                    palavrasList.append(len(label.split()))
            elif label == '...':
                pausaList.append(stop - start)
    durationListTotal += durationList
    pausaListTotal += pausaList
    palavrasListTotal += palavrasList

    segmentoMax = max(durationList)
    segmentoMin = min(durationList)
    segmentoMedia = Average(durationList)
    print(f'Tempo médio dos segmentos: {segmentoMedia}')
    print(f'Tempo máximo dos segmentos: {segmentoMax}')
    print(f'Tempo mínimo dos segmentos: {segmentoMin}\n')

    pausaMax = max(pausaList)
    pausaMin = min(pausaList)
    pausaMedia = Average(pausaList)
    print(f'Tempo médio das pausas: {pausaMedia}')
    print(f'Tempo máximo das pausas: {pausaMax}')
    print(f'Tempo mínimo das pausas: {pausaMin}\n')

    palavrasMedia = round(Average(palavrasList))
    palavrasMax= max(palavrasList)
    palavrasMin = min(palavrasList)
    print(f'Média das palavras: {palavrasMedia}')
    print(f'Máximo das palavras: {palavrasMax}')
    print(f'Mínimo das palavras: {palavrasMin}')
    print(f'{palavrasList}\n')

    print('------------------------------------------\n')

print('Média de todos os arquvios:')
print(f'Tempo médio de segmento: {Average(durationListTotal)}')
print(f'Tempo médio de pausa: {Average(pausaListTotal)}')
print(f'Média de palavras por segmento (arredondando): {round(Average(palavrasList))}')