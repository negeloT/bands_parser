# coding=utf-8
import arcpy
from arcpy.sa import *
import os

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Bands Parser"
        self.alias = ""
        self.tools = [Bands_Parser]


class Bands_Parser(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Bands_Parser"
        self.description = ""
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        raster = arcpy.Parameter(
            displayName="Multiband raster",
            name="raster",
            datatype="DERasterBand",
            parameterType="Required",
            direction="Input")

        bands = arcpy.Parameter(
            displayName="Raster bands",
            name="bands",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=True
        )
        bands.filter.type = "ValueList"
        bands.filter.list = []

        folder = arcpy.Parameter(
            displayName="Folder for saving bands",
            name="folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        params = [raster, bands, folder]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        if parameters[0].value:
            raster_path = parameters[0].valueAsText
            raster = arcpy.Raster(raster_path)
            band_names = []
            for idx in range(1, raster.bandCount + 1):
                name = "Band_{}".format(idx)
                band_names.append(name)
            parameters[1].filter.list = band_names
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        raster_path = parameters[0].valueAsText
        bands_selected = parameters[1].valueAsText.split(";")
        out_folder = parameters[2].valueAsText

        raster = arcpy.Raster(raster_path)

        for band_name in bands_selected:
            band_index = int(band_name.split("_")[-1].replace("'",""))
            band_raster = arcpy.Raster(raster_path + "/Band_" + str(band_index))
            out_name = "{}_Band_{}.tif".format(raster_path.split("\\")[-1].replace(".tif",""),band_index)
            out_path = os.path.join(out_folder, out_name)
            band_raster.save(out_path)

        return
