import wx
from GUI import MainFrame
import sys, logging

if __name__ == '__main__':
    logging.basicConfig(filename='Mod_loader.log', filemode='w')
    try:
        app = wx.App()
        window = MainFrame('Doom Mod Loader')
        window.Show()
        app.MainLoop()
    except:
        e = str(sys.exc_info()[0]) + str(sys.exc_info()[1])
        logging.error(e)
