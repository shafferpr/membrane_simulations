import sys
OpenDatabase(sys.argv[1])
#OpenDatabase("membrane/wall.xmf")
AddPlot("Contour", "sdf")
a=ContourAttributes()
a.SetContourNLevels(1)
SetPlotOptions(a)
#c0 = GetView3D()
v = GetView3D()
#v.viewNormal = (-0.571619, 0.405393, 0.713378)
v.viewNormal = (0.7983424994249126, -0.33921340156793495, -0.497577654048787)
v.viewUp = (0.5491548358410169, 0.7491733756992088, 0.3703622813082861)
SetView3D(v)
#c0.viewAngle = 30
#SetView3D(c0)
DrawPlots()
SaveWindow()
quit()
