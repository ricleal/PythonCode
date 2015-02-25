'''
Created on Feb 24, 2015

@author: leal
'''


#!/usr/bin/env python

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
        
        
 
    def create_intersection(self):
        
        sphereSource = vtk.vtkSphereSource()
        sphereSource.Update()
         
        bounds = [0 for _ in range(6)]
        sphereSource.GetOutput().GetBounds(bounds)
         
        box = vtk.vtkPoints()
        box.SetNumberOfPoints(8)
         
        xMin = bounds[0]; xMax = bounds[1]
        yMin = bounds[2]; yMax = bounds[3]
        zMin = bounds[4]; zMax = bounds[5]
         
        box.SetPoint(0, xMax, yMin, zMax)
        box.SetPoint(1, xMax, yMin, zMin)
        box.SetPoint(2, xMax, yMax, zMin)
        box.SetPoint(3, xMax, yMax, zMax)
        box.SetPoint(4, xMin, yMin, zMax)
        box.SetPoint(5, xMin, yMin, zMin)
        box.SetPoint(6, xMin, yMax, zMin)
        box.SetPoint(7, xMin, yMax, zMax)
         
        planesIntersection = vtk.vtkPlanesIntersection()
        planesIntersection.SetBounds(bounds)
         
        intersects = planesIntersection.IntersectsRegion(box)
         
        print "Intersects? " , intersects == 1
        
        self._add_source_to_render(sphereSource)
        
    
    def _add_source_to_render(self,source):
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
    o.create_intersection()   
    o.view()