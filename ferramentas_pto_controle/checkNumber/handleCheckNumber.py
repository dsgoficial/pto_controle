from collections import defaultdict
import csv
import os

class HandleCheckNumber():
    def checkNumber(self, layer, folder):
        lista_de_codigos = []
        for feature in layer.getFeatures():
            lista_de_codigos.append(feature['cod_ponto'])
        numeros_faltantes_por_grupo = findMissing(lista_de_codigos)
        saveCSV(numeros_faltantes_por_grupo, folder)

def findMissing(lista):
    grupos = defaultdict(list)
    for item in lista:
        partes = item.split('-')
        grupo, numero = '-'.join(partes[:-1]), int(partes[-1])
        grupos[grupo].append(numero)
    numeros_faltantes_por_grupo = {}
    for grupo, numeros in grupos.items():
        max_num = max(numeros)
        numeros_completos = set(range(1, max_num + 1))
        numeros_faltantes = list(numeros_completos - set(numeros))
        numeros_faltantes_por_grupo[grupo] = numeros_faltantes
    return numeros_faltantes_por_grupo

def saveCSV(numeros_faltantes_por_grupo, folder):
    csv_file_path = os.path.join(folder, 'pontos_faltantes.csv')
    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Grupo', 'Numero Faltante'])
        for grupo, numeros_faltantes in numeros_faltantes_por_grupo.items():
            for numero in numeros_faltantes:
                csv_writer.writerow([grupo, numero])