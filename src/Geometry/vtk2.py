'''
Created on Feb 24, 2015

@author: leal
'''

import vtk
 
class Objects():
    def __init__(self):
        # create a rendering window and renderer
        self.render = vtk.vtkRenderer()
        self.render_window = vtk.vtkRenderWindow()
        self.render_window.AddRenderer(self.render) 
        
        # create a renderwindowinteractor
        self.rennder_window_interactor = vtk.vtkRenderWindowInteractor()
        self.rennder_window_interactor.SetRenderWindow(self.render_window)
        
        
 
    def create_cylinder(self):
        # create source
        source = vtk.vtkCylinderSource()
        source.SetCenter(0,0,0)
        source.SetRadius(5.0)
        source.SetHeight(7.0)
        source.SetResolution(100.0)
        
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInput(source.GetOutput())
 
        # actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
 
        # assign actor to the renderer
        self.render.AddActor(actor)
        
    def create_arrow(self):
        source = vtk.vtkArrowSource()
        # Create a mapper and actor
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        
        self.render.AddActor(actor)

    def view(self):
        # enable user interface interactor
        self.rennder_window_interactor.Initialize()
        self.render_window.Render()
        self.rennder_window_interactor.Start()

if __name__ == '__main__':
    o = Objects()
    #o.create_cylinder()
    o.create_arrow()   
    o.view()