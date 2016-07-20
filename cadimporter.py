#-------------------------------------------------------------------------------
# Name:        CAD_Importer
# Purpose:     To move files from Sharepoint to the Enterprise Geodatabase,
#              renaimg the reserved fields from the CAD format
# Author:      CBrown
#
# Created:     27/06/2016
# Copyright:   (c) CBrown 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os
import string

cols = ['CAD_file', 'upload', 'project', 'dio', 'user']

# messages
NO_METADATA_MSG = "No metadata has been provided, please fill in."
NO_COORDS_MSG = "No coordinate system has been found. . . "
OTHER_COORDS_MSG = "CAD File is in other coordinate system: "
ASSUME_WGS84Z16N = "  Assumed WGS84 UTM Zone 16 North"
DEF_PROJECT_MSG = "  Define Projection to WGS84 UTM Zone 16 North"
REPROJECT = "  Reprojecting data to project coordinate system"

#define global variables
CAD_file = ""
upload = ""
project = ""
dio = ""
user = ""


def getParam(param):
    """
    Lookup a parameter by name, so that reordering or modification doesn't
    force changing the rest of the code.
    """
    return arcpy.GetParameterAsText(cols.index(param))


def checkCoords(CAD_file):
    spatial_ref = arcpy.Describe(CAD_file).spatialReference
    sr = arcpy.SpatialReference("WGS 1984 UTM Zone 16N")
    try:
        if spatial_ref == "Unknown":
            print(NO_COORDS_MSG)
            print("{0} has an unknkown spatial reference".format(fc))
            arcpy.DefineProjection_management(CAD_File, sr)
            print(DEF_PROJECT)
        elif spatial_ref != sr:
            print(OTHER_COORDS_MSG, spatial_ref)
            print (DEF_PROJECT_MSG)
            arcpy.Project_management(CAD_file,CAD_file+"_WGS84z16N",sr,"NONE",spatial_ref)
            CAD_file = CAD_file+"_WGS84z16N"
            print(REPROJECT)
        else:
            print("Coordinate System Check . . . . . OK")

    except:
        print(arcpy.GetMessages)

def cad2fgdb(CAD_file, scratch_path, project, dio, user):
    #pass global variables to local variables
    Project_Number = project
    DIO_Site_Number = dio
    Requested_By = user
    Input_CAD_Datasets = CAD_file
    Dataset = os.path.splitext(CAD_file)[0]
#    DatasetNum = ((string.rfind(Dataset, "\\"))+1)
    Dataset = Dataset[((string.rfind(Dataset, "\\"))+1):]
    Output_Feature_Dataset = Dataset
    Pending_Workspace = scratch_path
    Output_Folder = Pending_Workspace
    Output_Folder__2_ = Output_Folder
    v_Requested_By__gdb = Output_Folder__2_

    print "Input Pending Workspace = " + Pending_Workspace
    print "Input Project Number = " + project

    # Process: Create Project Folder
    if os.path.exists(Pending_Workspace + "\\" + project) == "False":
        arcpy.CreateFolder_management(Pending_Workspace, project)
        print "Created new Folder at " + Pending_Workspace + project

    Pending_Workspace = Pending_Workspace + "\\" + project
    print ". . . connected to folder " + Pending_Workspace

    # Process: Create DIO Folder
    if os.path.exists(Pending_Workspace + "\\" + DIO_Site_Number) == "False":
        arcpy.CreateFolder_management(Output_Folder, DIO_Site_Number)
        print "Created new Folder at " + Pending_Workspace + DIO_Site_Number

    Pending_Workspace = Pending_Workspace + "\\" + DIO_Site_Number
    print ". . . connected to folder " + Pending_Workspace


    # Process: Create Temporary File GDB
    if os.path.isfile(Pending_Workspace + "\\" + user + ".gdb") =="False":
        arcpy.CreateFileGDB_management(Pending_Workspace, user, "CURRENT")

    GeoDB = Pending_Workspace + "\\" + user + ".gdb"
    print "All data will be written to " + GeoDB
    print ". . . starting to interrogate " + Dataset
    print "CAD to Geodatabase (" + Input_CAD_Datasets + ", " + GeoDB + ", " + Dataset + ", 1000 , True)"
    # Process: CAD to Geodatabase
#    arcpy.CADToGeodatabase_conversion(Input_CAD_Datasets, GeoDB, Dataset, "1000", "True")

    arcpy.CADToGeodatabase_conversion(CAD_file, GeoDB, Dataset, "1000", "")


    # Load required toolboxes
    arcpy.ImportToolbox("Model Functions")

    # Script arguments
    CAD_Feature_Dataset = Output_Feature_Dataset # provide a default value if unspecified
    Output_Feature_Class = GeoDB + Dataset  # provide a default value if unspecified

    if Field_Name == '#' or not Field_Name:
        Field_Name = "Entity" # provide a default value if unspecified

    New_Field_Name = arcpy.GetParameterAsText(3)
    if New_Field_Name == '#' or not New_Field_Name:
        New_Field_Name = "CAD_Entity" # provide a default value if unspecified

    # Local variables:
    #Feature_Class = "\\\\nchk03sql02.hkncgis.com\\uploads\\HKND\\HKND-01\\cbrown.gdb\\CAD\\Polyline"
    #Name = F

    # Process: Iterate Feature Classes
    arcpy.IterateFeatureClasses_mb(CAD_Feature_Dataset, "", "", "NOT_RECURSIVE")

    # Process: Alter Field
    arcpy.AlterField_management(Feature_Class, Field_Name, New_Field_Name, "", "TEXT", "16", "NULLABLE", "false")

def fds2layer(path, fds, layername) :

    # Load required toolboxes
    arcpy.ImportToolbox("Model Functions")

    # Script arguments
    Feature_Dataset_or_Workspace = fds
    if Feature_Dataset_or_Workspace == '#' or not Feature_Dataset_or_Workspace:
        Feature_Dataset_or_Workspace = "\\\\nchk03sql02.hkncgis.com\\data\\Analysis\\Data Import\\CAD\\PRE1002-1\\CAD_Data.gdb\\CAD" # provide a default value if unspecified

    Layer_Output = path + "\\" + fds
    if Layer_Output == '#' or not Layer_Output:
        Layer_Output = "%Name%" # provide a default value if unspecified

    Output_Layer_File = fds

    # Local variables:
    Feature_Type__2_ = ""
    Name = Feature_Type__2_
    Feature_Type = ""

    # Process: Iterate Feature Classes
    arcpy.IterateFeatureClasses_mb(Feature_Dataset_or_Workspace, "", Feature_Type__2_, "RECURSIVE")

    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(Feature_Type, Layer_Output, "", "", "OBJECTID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Entity Entity VISIBLE NONE;Handle Handle VISIBLE NONE;Layer Layer VISIBLE NONE;LyrFrzn LyrFrzn VISIBLE NONE;LyrLock LyrLock VISIBLE NONE;LyrOn LyrOn VISIBLE NONE;LyrVPFrzn LyrVPFrzn VISIBLE NONE;LyrHandle LyrHandle VISIBLE NONE;Color Color VISIBLE NONE;EntColor EntColor VISIBLE NONE;LyrColor LyrColor VISIBLE NONE;BlkColor BlkColor VISIBLE NONE;Linetype Linetype VISIBLE NONE;EntLinetype EntLinetype VISIBLE NONE;LyrLnType LyrLnType VISIBLE NONE;BlkLinetype BlkLinetype VISIBLE NONE;Elevation Elevation VISIBLE NONE;Thickness Thickness VISIBLE NONE;LineWt LineWt VISIBLE NONE;EntLineWt EntLineWt VISIBLE NONE;LyrLineWt LyrLineWt VISIBLE NONE;BlkLineWt BlkLineWt VISIBLE NONE;RefName RefName VISIBLE NONE;LTScale LTScale VISIBLE NONE;Angle Angle VISIBLE NONE;ExtX ExtX VISIBLE NONE;ExtY ExtY VISIBLE NONE;ExtZ ExtZ VISIBLE NONE;DocName DocName VISIBLE NONE;DocPath DocPath VISIBLE NONE;DocType DocType VISIBLE NONE;DocVer DocVer VISIBLE NONE;ScaleX ScaleX VISIBLE NONE;ScaleY ScaleY VISIBLE NONE;ScaleZ ScaleZ VISIBLE NONE")

    # Process: Save To Layer File
    arcpy.SaveToLayerFile_management(Layer_Output, Output_Layer_File, "", "CURRENT")

def main():
    pass

if __name__ == '__main__':
    main()
upload ="\\\\nchk03sql02.hkncgis.com\\uploads"
CAD_file = r"C:\Users\CBrown\OneDrive - CSA GLOBAL PTY LTD\Projects\HKND\CAD\bmt_port_2_lane_30m_int.dxf"
path = upload + project + dio
print path
checkCoords(r"C:\Users\CBrown\OneDrive - CSA GLOBAL PTY LTD\Projects\HKND\CAD\bmt_port_2_lane_30m_int.dxf")
print arcpy.Describe(CAD_file).baseName

cad2fgdb(CAD_file,upload,"HKNDCADTest", "HKNDCADTest-01", "cbrown")

fcs = arcpy.gp.ListFeatureClasses()

#for fc in fcs:
#    print fc
fc = arcpy.gp.listFeatureClasses()
for fc in fcs:
    print fc

#fds2layer(path, path + "\\" + user + ".gdb\\CAD", CAD_file)

