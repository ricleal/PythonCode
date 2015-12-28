from numpy import arange, sin, pi
import matplotlib
matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.backends.backend_wxagg import Toolbar
from matplotlib.figure import Figure

import wx

class CanvasPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = Toolbar(self.canvas) #matplotlib toolbar
        self.toolbar.Realize()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        #self.sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        self.sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL)
        # Best to allow the toolbar to resize!
        self.sizer.Add(self.toolbar, 0, wx.GROW)
        self.SetSizer(self.sizer)
        self.Fit()

    def GetToolBar(self):
        # You will need to override GetToolBar if you are using an
        # unmanaged toolbar in your frame
        return self.toolbar

    def draw(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2 * pi * t)
        self.axes.plot(t, s)

    def OnPaint(self, event):
        self.canvas.draw()


if __name__ == "__main__":
    app = wx.PySimpleApp()
    fr = wx.Frame(None, title='test')
    panel = CanvasPanel(fr)
    panel.draw()
    fr.Show()
    size = fr.GetSize()
    fr.SetMinSize((size[0] / 2, size[1] / 2))
    app.MainLoop()
