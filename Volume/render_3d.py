import vtk
import numpy as np



class vtk3dRenderer():
    def __init__(self, data_matrix):
        self.data_matrix = data_matrix
        self.data_center = np.array(data_matrix.shape)/2
        
        print "Shape:", data_matrix.shape
        print "Max:", np.max(data_matrix)
        print "Min:", np.min(data_matrix)
        self.data_min =  np.min(data_matrix)
        self.data_max =  np.max(data_matrix)
        
    def initialise(self):
        dataImporter = vtk.vtkImageImport()
        data_string = self.data_matrix.tostring()
        dataImporter.CopyImportVoidPointer(data_string, len(data_string))
        dataImporter.SetDataScalarTypeToUnsignedChar()
        dataImporter.SetNumberOfScalarComponents(1)
        dataImporter.SetDataExtent(0, self.data_matrix.shape[0]-1,
                                   0, self.data_matrix.shape[1]-1,
                                   0, self.data_matrix.shape[2]-1)
        dataImporter.SetWholeExtent(0, self.data_matrix.shape[0]-1,
                                   0, self.data_matrix.shape[1]-1,
                                   0, self.data_matrix.shape[2]-1)
        
        
        alphaChannelFunc = vtk.vtkPiecewiseFunction()
        colorFunc = vtk.vtkColorTransferFunction()
        
        for i in range(int(self.data_min),int(self.data_max)):
            alphaChannelFunc.AddPoint(i, i/self.data_max )
            colorFunc.AddRGBPoint(i,i/self.data_max,i/self.data_max,i/self.data_max)
        # for our test sample, we set the black opacity to 0 (transparent) so as
        #to see the sample  
        alphaChannelFunc.AddPoint(0, 0.0)
        colorFunc.AddRGBPoint(0,0,0,0)


        
        
        
        
        
        
        
        
        
         
#         alphaChannelFunc = vtk.vtkPiecewiseFunction()
#         alphaChannelFunc.AddPoint(self.data_min, 0.0)
#         alphaChannelFunc.AddPoint(self.data_max - self.data_min /2, 0.1)
#         alphaChannelFunc.AddPoint(self.data_max, 0.2)
#          
#         # This class stores color data and can create color tables from a few color points. For this demo, we want the three cubes
#         # to be of the colors red green and blue.
#         colorFunc = vtk.vtkColorTransferFunction()
#         colorFunc.AddRGBPoint(50, 1.0, 0.0, 0.0)
#         colorFunc.AddRGBPoint(100, 0.0, 1.0, 0.0)
#         colorFunc.AddRGBPoint(150, 0.0, 0.0, 1.0)
         
        # The preavius two classes stored properties. Because we want to apply these properties to the volume we want to render,
        # we have to store them in a class that stores volume prpoperties.
        volumeProperty = vtk.vtkVolumeProperty()
        volumeProperty.SetColor(colorFunc)
        volumeProperty.SetScalarOpacity(alphaChannelFunc)
         
        # This class describes how the volume is rendered (through ray tracing).
        compositeFunction = vtk.vtkVolumeRayCastCompositeFunction()
        # We can finally create our volume. We also have to specify the data for it, as well as how the data will be rendered.
        volumeMapper = vtk.vtkVolumeRayCastMapper()
        volumeMapper.SetVolumeRayCastFunction(compositeFunction)
        volumeMapper.SetInputConnection(dataImporter.GetOutputPort())
         
        # The class vtkVolume is used to pair the preaviusly declared volume as well as the properties to be used when rendering that volume.
        self.volume = vtk.vtkVolume()
        self.volume.SetMapper(volumeMapper)
        self.volume.SetProperty(volumeProperty)

    @staticmethod
    def __exitCheck(obj, event):
            if obj.GetEventPending() != 0:
                obj.SetAbortRender(1)
    
    def render(self):
        # With almost everything else ready, its time to initialize the renderer and window, as well as creating a method for exiting the application
        renderer = vtk.vtkRenderer()
        renderWin = vtk.vtkRenderWindow()
        renderWin.AddRenderer(renderer)
        renderInteractor = vtk.vtkRenderWindowInteractor()
        renderInteractor.SetRenderWindow(renderWin)
         
        # We add the volume to the renderer ...
        renderer.AddVolume(self.volume)
        # ... set background color to white ...
        renderer.SetBackground(0,0,0)
        # ... and set window size.
        renderWin.SetSize(400, 400)
         
        # A simple function to be called when the user decides to quit the application.
        
         
        # Tell the application to use the function as an exit check.
        renderWin.AddObserver("AbortCheckEvent", vtk3dRenderer.__exitCheck)
         
        renderInteractor.Initialize()
        # Because nothing will be rendered without any input, we order the first render manually before control is handed over to the main-loop.
        renderWin.Render()
        renderInteractor.Start()
    

def V(x, y, z):
    """ A 3D sinusoidal lattice with a parabolic confinement. """
    return np.cos(10*x) + np.cos(10*y) + np.cos(10*z) + 2*(x**2 + y**2 + z**2)
        
if __name__ == '__main__':
    X, Y, Z = np.mgrid[-2:2:100j, -2:2:100j, -2:2:100j]    
    data = V(X, Y, Z)
    r = vtk3dRenderer(data)
    r.initialise()
    r.render()
    

# An example from scipy cookbook demonstrating the use of numpy arrys in vtk 
 

 

 
