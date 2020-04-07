import os
import vtk
import shutil

class Generate:

    def __init__(self, path):
        self.path = path
        self.ID   = -1

    def getID(self):
        return self.ID

    def __incrID(self):
        self.ID += 1

        return self.ID

    def populate(self, rWin, cameras):
        """Given a VTK render window, populate a cinema database
        """
        if os.path.isdir(self.path):
            shutil.rmtree(self.path)

        theCamera = rWin.GetRenderers().GetFirstRenderer().GetActiveCamera()

        # make a new database
        os.makedirs(self.path)
        with open(os.path.join(self.path, "data.csv"), "w", newline='\n') as dfile:
            dfile.write("phi,theta,FILE\n")
            for c in cameras:
                theCamera.Azimuth(c['phi'])
                theCamera.Elevation(c['theta'])
                rWin.Render()
                w2i = vtk.vtkWindowToImageFilter()
                iw = vtk.vtkPNGWriter()
                w2i.SetInput(rWin)
                iw.SetInputConnection(w2i.GetOutputPort())
                w2i.Update()

                cID = self.__incrID()
                dfile.write("{},{},{}.png\n".format(c['phi'], c['theta'], "{:04d}".format(cID)))
                iw.SetFileName(os.path.join(self.path, "{:04d}.png".format(cID)))
                iw.Write()

