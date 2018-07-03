import os
import shutil
from subprocess import run


class EpsFile:
    r = '.eps'

    def __init__(self, f):
        self.f = f

    def get_folder_name(self):
        folder_name = self.f.replace(self.r, '')
        return folder_name

    def copy_file(self, folder_name):
        shutil.copy(self.f, os.path.join(folder_name, self.f))

    def process(self):
        folder_name = self.get_folder_name()
        self.copy_file(folder_name)


class JpgFile(EpsFile):
    r = '.jpg'

    def process(self):
        folder_name = self.get_folder_name()
        try:
            os.mkdir(folder_name)
        except FileExistsError:
            print(f'{folder_name}. Такая папка уже есть')
        finally:
            self.copy_file(folder_name)


class Groupper:

    def __init__(self, FileType):
        self.FileType = FileType

    def get_all_files(self):
        all_f = [f for f in os.listdir() if os.path.isfile(f) and self.FileType.r in f]
        return all_f

    def process(self):
        all_files = self.get_all_files()
        for f in all_files:
            f_obj = self.FileType(f)
            f_obj.process()


class ZipperCreator:

    zipper_name = 'zipper.bat'

    def __init__(self, settings_file_name = 'settings.txt'):
        self.settings_file_name = settings_file_name

    def get_path_to_7z(self):
        # читаем путь из файла настроек
        try:
            with open(self.settings_file_name) as f:
                path_to_7z = f.read()
                return path_to_7z
        except FileNotFoundError:
            # то возвращаем путь по умолчанию
            return 'c:\\Program Files\\7-Zip\\7z.exe'

    def create(self):
        path_to_7z = self.get_path_to_7z()
        # создаем файл для zip архива если его нету
        # путь до 7zip будем задавать параметром, вдруг его нету
        with open(self.zipper_name, 'w') as f:
            # формируем строку
            run_str = f'for /d %%X in (*) do "{path_to_7z}" a "%%X.zip" "%%X\\"'
            f.write(run_str)


for f in (JpgFile, EpsFile):
    g = Groupper(f)
    g.process()

# читаем путь до 7zip из файла настроек

zc = ZipperCreator()
zc.create()

# попробуем в подпроцессе запустить батник
run(zc.zipper_name)
