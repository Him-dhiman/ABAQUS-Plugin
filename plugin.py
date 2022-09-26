from abaqus import *
from abaqusConstants import *

def createMandrel(partName,inner_radius,outer_radius,length,composite_thickness,material1_pos,material1_young,e1,e2,e3,u1,u2,u3,g1,g2,g3):
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.sketchOptions.setValues(viewStyle=AXISYM)
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])

    #start of inner structure of Part-1
    s.ArcByCenterEnds(center=(0.0, length+inner_radius), point1=(0.0, length+2*inner_radius), point2=(inner_radius, length+inner_radius), direction=CLOCKWISE)
    s.CoincidentConstraint(entity1=v[2], entity2=g[2], addUndoState=False)
    s.CoincidentConstraint(entity1=v[0], entity2=g[2], addUndoState=False)
    s.ArcByCenterEnds(center=(0.0, inner_radius), point1=(0.0, 0.0), point2=(inner_radius, inner_radius), direction=COUNTERCLOCKWISE)
    s.CoincidentConstraint(entity1=v[5], entity2=g[2], addUndoState=False)
    s.CoincidentConstraint(entity1=v[3], entity2=g[2], addUndoState=False)
    s.Line(point1=(inner_radius, length+inner_radius), point2=(inner_radius, inner_radius))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    s.TangentConstraint(entity1=g[3], entity2=g[5], addUndoState=False)
    s.offset(distance=outer_radius-inner_radius, objectList=(g[3], g[4], g[5]), side=LEFT) #check offset value later
    s.Line(point1=(0.0, length+2*inner_radius), point2=(0.0, length+inner_radius+outer_radius))
    s.VerticalConstraint(entity=g[9], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[9], addUndoState=False)
    s.Line(point1=(0.0, 0.0), point2=(0.0, -(outer_radius-inner_radius)))
    # end of inner structure of Part-1

    s.VerticalConstraint(entity=g[10], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[4], entity2=g[10], addUndoState=False)
    p = mdb.models['Model-1'].Part(name='Part-1', dimensionality=AXISYMMETRIC, type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Part-1']
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    p1 = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    p = mdb.models['Model-1'].Part(name='composite', 
        objectToCopy=mdb.models['Model-1'].parts['Part-1'])
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['Model-1'].parts['composite']
    s1 = p.features['Shell planar-1'].sketch
    mdb.models['Model-1'].ConstrainedSketch(name='__edit__', objectToCopy=s1)
    s2 = mdb.models['Model-1'].sketches['__edit__']
    g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
    s2.setPrimaryObject(option=SUPERIMPOSE)
    p.projectReferencesOntoSketch(sketch=s2, 
        upToFeature=p.features['Shell planar-1'], filter=COPLANAR_EDGES)
    s2.autoTrimCurve(curve1=g[5], point1=(4.95697784423828, 16.4795475006104))
    s2.autoTrimCurve(curve1=g[3], point1=(2.49674224853516, 28.7489490509033))
    s2.autoTrimCurve(curve1=g[4], point1=(3.36505889892578, 1.82843780517578))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=54.9855, 
        farPlane=70.951, width=61.2505, height=22.4553, cameraPosition=(2.19602, 
        16.9697, 62.9682), cameraTarget=(2.19602, 16.9697, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=54.476, 
        farPlane=71.4605, cameraPosition=(1.79666, 30.9606, 62.9682), 
        cameraTarget=(1.79666, 30.9606, 0))
    session.viewports['Viewport: 1'].view.setValues(nearPlane=53.9339, 
        farPlane=72.0025)
    s2.autoTrimCurve(curve1=g[9], point1=(-0.225057125091553, 29.7407455444336))
    
    s2.offset(distance=composite_thickness, objectList=(g[7], g[8], g[13]), side=LEFT)
    s2.Line(point1=(0.0, inner_radius+outer_radius+length+composite_thickness), point2=(0.0, inner_radius+outer_radius+length))
    s2.VerticalConstraint(entity=g[17], addUndoState=False)
    s2.PerpendicularConstraint(entity1=g[14], entity2=g[17], addUndoState=False)
    s2.Line(point1=(0.0, -(outer_radius-inner_radius+composite_thickness)), point2=(0.0, -(outer_radius-inner_radius)))
    s2.VerticalConstraint(entity=g[18], addUndoState=False)
    s2.PerpendicularConstraint(entity1=g[16], entity2=g[18], addUndoState=False)
    s2.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['composite']
    p.features['Shell planar-1'].setValues(sketch=s2)
    del mdb.models['Model-1'].sketches['__edit__']
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON)
    session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
        referenceRepresentation=OFF)
    mdb.models['Model-1'].Material(name='Material-1')
    mdb.models['Model-1'].materials['Material-1'].Elastic(table=((material1_young, material1_pos),))
    mdb.models['Model-1'].Material(name='Material-2')
    mdb.models['Model-1'].materials['Material-2'].Elastic(
        type=ENGINEERING_CONSTANTS, table=((e1, e2, e3, u1, u2, u3, g1, g2, g3), ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
        material='Material-1', thickness=None)
    p = mdb.models['Model-1'].parts['composite']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(faces=faces, name='Set-1')
    p = mdb.models['Model-1'].parts['composite']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    p = mdb.models['Model-1'].parts['composite']
    p.regenerate()
    p = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    mdb.models['Model-1'].HomogeneousSolidSection(name='Section-2', 
        material='Material-1', thickness=None)
    p = mdb.models['Model-1'].parts['Part-1']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(faces=faces, name='Set-1')
    p = mdb.models['Model-1'].parts['Part-1']
    p.SectionAssignment(region=region, sectionName='Section-2', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    mdb.models['Model-1'].sections['Section-1'].setValues(material='Material-2', 
        thickness=None)
    p = mdb.models['Model-1'].parts['composite']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['Model-1'].parts['composite']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(faces=faces, name='Set-2')
    p = mdb.models['Model-1'].parts['composite']
    p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    p = mdb.models['Model-1'].parts['composite']
    p.DatumCsysByThreePoints(name='Datum csys-1', coordSysType=CARTESIAN, origin=(
        0.0, 0.0, 0.0), line1=(1.0, 0.0, 0.0), line2=(0.0, 1.0, 0.0))
    p = mdb.models['Model-1'].parts['composite']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region = regionToolset.Region(faces=faces)
    orientation = mdb.models['Model-1'].parts['composite'].datums[4]
    mdb.models['Model-1'].parts['composite'].MaterialOrientation(region=region, 
        orientationType=SYSTEM, axis=AXIS_3, localCsys=orientation, fieldName='', 
        additionalRotationType=ROTATION_NONE, angle=0.0, 
        additionalRotationField='', stackDirection=STACK_3)
    #: Specified material orientation has been assigned to the selected regions.
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
    a = mdb.models['Model-1'].rootAssembly
    a.DatumCsysByThreePoints(coordSysType=CYLINDRICAL, origin=(0.0, 0.0, 0.0), 
        point1=(1.0, 0.0, 0.0), point2=(0.0, 0.0, -1.0))
    p = mdb.models['Model-1'].parts['Part-1']
    a.Instance(name='Part-1-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['composite']
    a.Instance(name='composite-1', part=p, dependent=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(
        adaptiveMeshConstraints=ON)
    mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
        constraints=ON, connectors=ON, engineeringFeatures=ON, 
        adaptiveMeshConstraints=OFF)
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['composite-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    leaf = dgm.LeafFromGeometry(faceSeq=faces1)
    session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=86.7364, 
        farPlane=114.495, width=95.0509, height=32.6835, viewOffsetX=1.55707, 
        viewOffsetY=0.124288)
    leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
    session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
        leaf=leaf)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=84.0879, 
        farPlane=117.144, width=125.559, height=43.1739, viewOffsetX=-2.69746, 
        viewOffsetY=0.378506)
    a = mdb.models['Model-1'].rootAssembly
    e1 = a.instances['Part-1-1'].edges
    edges1 = e1.getSequenceFromMask(mask=('[#e0 ]', ), )
    leaf = dgm.LeafFromGeometry(edgeSeq=edges1)
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['composite-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    leaf = dgm.LeafFromGeometry(faceSeq=faces1)
    session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
    leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
    session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
        leaf=leaf)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=94.5486, 
        farPlane=106.683, width=41.2928, height=14.1986, viewOffsetX=3.11537, 
        viewOffsetY=-1.20538)
    a = mdb.models['Model-1'].rootAssembly
    f1 = a.instances['Part-1-1'].faces
    faces1 = f1.getSequenceFromMask(mask=('[#1 ]', ), )
    leaf = dgm.LeafFromGeometry(faceSeq=faces1)
    session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.remove(leaf=leaf)
    session.viewports['Viewport: 1'].view.setValues(nearPlane=84.5575, 
        farPlane=116.674, width=120.639, height=41.4821, viewOffsetX=14.7698, 
        viewOffsetY=2.7536)
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Part-1-1'].edges
    side1Edges1 = s1.getSequenceFromMask(mask=('[#e0 ]', ), )
    region1=a.Surface(side1Edges=side1Edges1, name='m_Surf-1')
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['composite-1'].edges
    side1Edges1 = s1.getSequenceFromMask(mask=('[#7 ]', ), )
    region2=a.Surface(side1Edges=side1Edges1, name='s_Surf-1')
    mdb.models['Model-1'].Tie(name='Constraint-1', master=region1, slave=region2, 
        positionToleranceMethod=COMPUTED, adjust=ON, tieRotations=ON, thickness=ON)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
        predefinedFields=ON, interactions=OFF, constraints=OFF, 
        engineeringFeatures=OFF)
    leaf = dgm.Leaf(leafType=DEFAULT_MODEL)
    session.viewports['Viewport: 1'].assemblyDisplay.displayGroup.replace(
        leaf=leaf)
    a = mdb.models['Model-1'].rootAssembly
    s1 = a.instances['Part-1-1'].edges
    side1Edges1 = s1.getSequenceFromMask(mask=('[#e ]', ), )
    region = a.Surface(side1Edges=side1Edges1, name='Surf-3')
    mdb.models['Model-1'].Pressure(name='Load-1', createStepName='Step-1', 
        region=region, distributionType=UNIFORM, field='', magnitude=20.0, 
        amplitude=UNSET)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
        bcs=OFF, predefinedFields=OFF, connectors=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=ON)
    p = mdb.models['Model-1'].parts['composite']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
        engineeringFeatures=OFF, mesh=ON)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=ON)
    p = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['Model-1'].parts['Part-1']
    p.seedPart(size=1.0, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-1'].parts['Part-1']
    p.generateMesh()
    p = mdb.models['Model-1'].parts['composite']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    p = mdb.models['Model-1'].parts['composite']
    p.seedPart(size=2.0, deviationFactor=0.1, minSizeFactor=0.1)
    p = mdb.models['Model-1'].parts['composite']
    p.generateMesh()
    a1 = mdb.models['Model-1'].rootAssembly
    a1.regenerate()
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
    session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
        engineeringFeatures=ON, mesh=OFF)
    session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
        meshTechnique=OFF)
    p1 = mdb.models['Model-1'].parts['composite']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    del mdb.models['Model-1'].parts['composite'].sectionAssignments[0]
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
    #: The job input file "Job-1.inp" has been submitted for analysis.
    #: Job Job-1: Analysis Input File Processor completed successfully.
    #: Job Job-1: Abaqus/Standard completed successfully.
    #: Job Job-1 completed successfully. 
    o3 = session.openOdb(name='C:/temp/Job-1.odb')
    #: Model: C:/temp/Job-1.odb
    #: Number of Assemblies:         1
    #: Number of Assembly instances: 0
    #: Number of Part instances:     2
    #: Number of Meshes:             2
    #: Number of Element Sets:       4
    #: Number of Node Sets:          4
    #: Number of Steps:              1
    session.viewports['Viewport: 1'].setValues(displayedObject=o3)
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        CONTOURS_ON_DEF, ))
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        DEFORMED, ))
    mdb.saveAs(pathName='C:/temp/mandrelfinal')
    #: The model database has been saved to "C:\temp\mandrelfinal.cae".
