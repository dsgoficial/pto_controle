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
        for folder in self.folders:
            point = folder.parts[-1]
            try:
                shutil.copy(str(Path(self.aer_view / f'{point}.jpg')), str(
                    folder / '7_Imagens_Monografia' / f'{point}_AEREA.jpg'))
                shutil.copy(str(Path(self.view1 / f'{point}.jpg')), str(
                    folder / '7_Imagens_Monografia' / f'{point}_MUNICIPIO.jpg'))
                shutil.copy(str(Path(self.view2 / f'{point}.jpg')), str(
                    folder / '7_Imagens_Monografia' / f'{point}_ESTADO.jpg'))
            except IOError as err:
                print(err)


if __name__ == "__main__":
    handle = HandleDistributeImages(*sys.argv[1:])
    handle.create_folder()
    handle.distribute_images()
