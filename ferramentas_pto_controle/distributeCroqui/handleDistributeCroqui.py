from pathlib import Path
import re
import sys
import shutil


# O MESMO padrao que o P02 cobra da estrutura de pastas, e por isso o contrato.
# O anterior era r'\w\w-\w\w-0*\d+', que exige exatamente DUAS letras no tipo e
# portanto deixava toda pasta BASE de fora, calada: SC-BASE-1 nao casava, e o
# ponto base ficava sem croqui digital sem nenhuma mensagem.
PASTA_DE_PONTO = re.compile(r'^[A-Z]{2}-(HV|Base|BASE)-[1-9][0-9]*$')


class HandleDistributeCroqui():

    def __init__(self, structure, folder_aer_view):
        self.folders = []
        self.structure = Path(structure)
        self.aer_view = Path(folder_aer_view)

    def create_folder(self):
        self.folders = [x for x in self.structure.rglob('*')
                        if x.is_dir() and PASTA_DE_PONTO.match(x.parts[-1])]
        for folder in self.folders:
            Path(folder / '4_Croqui').mkdir(exist_ok=True)

    def distribute_croqui(self):
        """Copia o croqui digital para a pasta 4_Croqui de cada ponto.

        Devolve a lista de falhas. Quem chama TEM de olhar essa lista: antes o
        erro so era impresso, entao o passo dizia 'concluido' sem ter copiado um
        croqui sequer. Foi assim que os tres defeitos de QGIS 4 ficaram invisiveis.
        """
        falhas = []
        for folder in self.folders:
            point = folder.parts[-1]
            origem = self.aer_view / f'{point}.jpg'
            try:
                shutil.copy(str(origem),
                            str(folder / '4_Croqui' / f'{point}_CROQUI_DIGITAL.jpg'))
            except (IOError, OSError) as err:
                falhas.append(f'{point}: {err}')
        return falhas


if __name__ == "__main__":
    handle = HandleDistributeCroqui(*sys.argv[1:])
    handle.create_folder()
    for falha in handle.distribute_croqui():
        print(falha)
