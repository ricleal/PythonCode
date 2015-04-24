import wx

########################################################################
class PanelTest(wx.Panel):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self, parent, text="Hello world"):
        """Constructor"""
        wx.Panel.__init__(self, parent=parent)
        txt = wx.StaticText(self,label=text, pos=(20, 30))
 

class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self, title="Main frame"):
        wx.Frame.__init__(self, None, wx.ID_ANY, title)
    def set_panel(self,panel):
        self.panel = panel

 
  
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    for i in range(2):
        frame = MyForm(title="Frame %s"%i)
        this_panel = PanelTest(frame, text = "This is panel %d"%i)
        frame.set_panel(this_panel)
        frame.Show()
    app.MainLoop()