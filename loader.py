import os


class Loader:
    def __init__(self):
        self.installed_mods = dict()

        file_list = os.listdir('.')
        for file in file_list:
            if '.ini' in file and 'gzdoom' in file:
                self.ini = file

        self.read_files()
        self.read_ini()

    def read_ini(self):
        with open(self.ini, 'r') as f:
            output = f.read()
        mods = output.split('[doom.Autoload]', 1)[1].split('[doom.id.Autoload]', 1)[0].split('path=mods\\')
        for mod in mods:
            mod = mod.replace('\n', '')
            if mod != '':
                if mod in self.installed_mods:
                    self.installed_mods[mod] = True

    def read_files(self):
        dir_list = os.listdir('mods')
        for filename in dir_list:
            if '.wad' in filename or '.pk3' in filename:
                self.installed_mods[filename] = False

    def set_installed(self, mods):
        for mod in mods:
            self.installed_mods[mod] = True

    def set_uninstalled(self, mods):
        for mod in mods:
            self.installed_mods[mod] = False

    def set_installed_exclusive(self, mods):
        for key in self.installed_mods:
            if key in mods:
                self.installed_mods[key] = True
            else:
                self.installed_mods[key] = False

    def get_mods(self):
        return self.installed_mods

    def save(self):
        with open(self.ini, 'r') as f:
            output = f.read()

        file_start = output.split('[doom.Autoload]', 1)[0] + '[doom.Autoload]\n'
        file_end = '[doom.id.Autoload]'+output.split('[doom.id.Autoload]', 1)[1]

        with open(self.ini, 'w') as f:
            f.write(file_start)
            for mod in self.installed_mods:
                if self.installed_mods[mod] is True:
                    f.write('path=mods\\'+mod+'\n')
            f.write('\n'+file_end)
