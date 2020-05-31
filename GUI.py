import wx
import os
from loader import Loader
import subprocess as sp


class MainFrame(wx.Frame):
    def __init__(self, title):
        super(MainFrame, self).__init__(None, title=title)

        try:
            self.mod_loader = Loader()
        except FileNotFoundError:
            textbox = wx.MessageDialog(None, "Couldn't find gzdoom config file, is the executable located in the game folder?", '.ini Not Found', wx.OK)
            textbox.ShowModal()
            self.Close()

        self.mod_list = list(self.mod_loader.get_mods().keys())
        self.mod_list.sort()

        self.init_UI()
        self.Centre()

    def init_UI(self):
        panel = wx.Panel(self)

        mainbox = wx.BoxSizer(wx.VERTICAL)

        self.checklist = wx.CheckListBox(parent=panel, id=wx.ID_ANY, choices=self.mod_list)
        self.init_list(self.checklist)
        staticBox = wx.StaticBox(panel, -1, label="Avaiable mods")
        sbsizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
        sbsizer.Add(self.checklist, flag=wx.EXPAND, proportion=1)
        mainbox.Add(sbsizer, flag=wx.EXPAND | wx.ALL, border=15, proportion=1)

        buttonbox = wx.GridBagSizer(1, 4)
        help_button = wx.Button(panel, -1, label='Help', size=(70, 30))
        help_button.Bind(wx.EVT_BUTTON, self.show_help)
        buttonbox.Add(help_button, pos=(0, 0), flag=wx.LEFT | wx.BOTTOM, border=10)

        run_button = wx.Button(panel, -1, label='Run', size=(70, 30))
        run_button.Bind(wx.EVT_BUTTON, self.run_mods)
        buttonbox.Add(run_button, pos=(0, 3), flag=wx.RIGHT | wx.BOTTOM, border=10)

        save_button = wx.Button(panel, -1, label='Save', size=(70, 30))
        save_button.Bind(wx.EVT_BUTTON, self.save_mods)
        buttonbox.Add(save_button, pos=(0, 2), flag=wx.RIGHT | wx.BOTTOM, border=10)
        buttonbox.AddGrowableCol(1)

        mainbox.Add(buttonbox, flag=wx.EXPAND)

        mainbox.SetSizeHints(panel)
        panel.SetSizer(mainbox)

    def init_list(self, checklist):
        installed = []
        for mod in self.mod_list:
            mods = self.mod_loader.get_mods()
            if mods[mod] is True:
                installed.append(mod)

            checklist.SetCheckedStrings(installed)

    def show_help(self, e):
        text = "Make sure this executable is located in the same folder as the doom executable\n\n" \
        "Make sure your mods are located in a folder called 'mods' inside the base installation folder\n\n" \
        "Check the mods you're wishing to play. The program doesn't check compatibility, " \
        "it's up to the user not to load incompatible mods.\n\n" \
        "Save - sets the selected mods in autoload so you can play them every time you run gzdoom\n\n" \
        "Run - runs gzdoom with the currently selected mods ignoring mods set in autoload"

        wx.MessageBox(text, 'Help', wx.OK)

    def save_mods(self, e):
        self.mod_loader.set_installed_exclusive(self.checklist.GetCheckedStrings())
        self.mod_loader.save()
        wx.MessageBox("Mods saved correctly!", 'Done!', wx.OK)
        self.Close()

    def run_mods(self, e):
        command = ['dosbox.exe', '-conf ./doom2m.conf', '-fullscreen', '-noautoload', '-file'] + \
                  [os.path.join("mods", mod) for mod in list(self.checklist.GetCheckedStrings())]
        sp.Popen(command)
        self.Close()
