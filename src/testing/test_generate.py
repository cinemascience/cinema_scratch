import unittest
import vtk
import cscratch
import os

class TestCIS(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCIS, self).__init__(*args, **kwargs)
        self.renWin = None
        self.cdb = ""

    def setUp(self):
        return

    def tearDown(self):
        clean = False
        if clean:
            os.system('rm -rf testing/scratch')
        else:
            print("not cleaning up")
        return

    def test_generate(self):
        self.__load_dataset()

        cameras = [
            {'phi':  0, 'theta':  0},
            {'phi': 15, 'theta':  0},
            {'phi': 30, 'theta':  0},
            {'phi': 45, 'theta':  0},
            {'phi':  0, 'theta': 15},
            {'phi': 15, 'theta': 15},
            {'phi': 30, 'theta': 15},
            {'phi': 45, 'theta': 15},
            {'phi':  0, 'theta': 30},
            {'phi': 15, 'theta': 30},
            {'phi': 30, 'theta': 30},
            {'phi': 45, 'theta': 30},
            {'phi':  0, 'theta': 45},
            {'phi': 15, 'theta': 45},
            {'phi': 30, 'theta': 45},
            {'phi': 45, 'theta': 45}
        ]
        self.cdb = "testing/scratch/test.cdb"
        generator = cscratch.generate.Generate(self.cdb)
        generator.populate(self.renWin, cameras)
        dbs = [
            {"path": "test.cdb"}
        ]
        cscratch.cinstall.install.install.explorer(
                "cscratch/cinstall/cinema.source",
                "testing/scratch", "explorer.html", dbs)

        # if you want to view the database
        os.system('open -a Firefox testing/scratch/explorer.html')



    def __load_dataset(self):
        fname = "../data/testdata.vti"
        reader = vtk.vtkXMLImageDataReader()
        reader.SetFileName( fname )
        reader.Update()

        ren = vtk.vtkRenderer()
        self.renWin = vtk.vtkRenderWindow()
        self.renWin.SetSize(1024, 768)
        self.renWin.AddRenderer(ren)

        # make the pipeline
        contour = vtk.vtkContourFilter()
        contour.SetValue(0, 220) 
        contour.SetInputConnection(reader.GetOutputPort())

        contourMapper = vtk.vtkPolyDataMapper()
        contourMapper.SetInputConnection(contour.GetOutputPort())

        contourActor = vtk.vtkActor()
        contourActor.SetMapper(contourMapper)
        contourActor.GetProperty().SetAmbient(0.8)
        contourActor.GetProperty().SetDiffuse(0.8)
        contourActor.GetProperty().SetSpecular(0.8)
        ren.AddActor(contourActor)

        ren.GetActiveCamera().SetPosition(0, 0, 50)

        return
