from pathlib import Path
import re
import sys
import shutil


class HandleDistributeImages():

    def __init__(self, structure, folder_aer_view, folder_view1, folder_view2):
        self.folders = []
        self.structure = Path(structure)
        self.aer_view = Path(folder_aer_view)
        self.view1 = Path(folder_view1)
        self.view2 = Path(folder_view2)

    def create_folder(self):
        self.folders = [x for x in self.structure.rglob(
            '*') if x.is_dir() and re.match(r'\w\w-\w\w-0*\d+', x.parts[-1])]
        for folder in self.folders:
            Path(folder / '7_Imagens_Monografia').mkdir(exist_ok=True)

    def distribute_images(self):
        """Copia as tres vistas para cada pasta de ponto.

        Devolve a lista de falhas. Quem chama TEM de olhar essa lista: antes o
        erro so era impresso, entao o P08 dizia 'concluido' mesmo sem ter copiado
        uma imagem sequer.
        """
        falhas = []
        for folder in self.folders:
            point = folder.parts[-1]
            destino = folder / '7_Imagens_Monografia'
            for origem, sufixo in [(self.aer_view, 'AEREA'),
                                   (self.view1, 'MUNICIPIO'),
                                   (self.view2, 'ESTADO')]:
                arquivo = origem / f'{point}.jpg'
                try:
                    shutil.copy(str(arquivo), str(destino / f'{point}_{sufixo}.jpg'))
                except (IOError, OSError) as err:
                    falhas.append(f'{point} {sufixo}: {err}')
        return falhas


if __name__ == "__main__":
    handle = HandleDistributeImages(*sys.argv[1:])
    handle.create_folder()
    for falha in handle.distribute_images():
        print(falha)
