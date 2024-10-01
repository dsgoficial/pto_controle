from pathlib import Path
import re
import sys
import shutil


class HandleDistributeCroqui():

    def __init__(self, structure, folder_aer_view):
        self.folders = []
        self.structure = Path(structure)
        self.aer_view = Path(folder_aer_view)

    def create_folder(self):
        self.folders = [x for x in self.structure.rglob(
            '*') if x.is_dir() and re.match(r'\w\w-\w\w-0*\d+', x.parts[-1])]
        for folder in self.folders:
            Path(folder / '4_Croqui').mkdir(exist_ok=True)

    def distribute_croqui(self):
        for folder in self.folders:
            point = folder.parts[-1]
            try:
                shutil.copy(str(Path(self.aer_view / f'{point}.jpg')), str(
                    folder / '4_Croqui' / f'{point}_CROQUI.jpg'))
            except IOError as err:
                print(err)


if __name__ == "__main__":
    handle = HandleDistributeCroqui(*sys.argv[1:])
    handle.create_folder()
    handle.distribute_croqui()
