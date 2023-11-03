import os
from osgeo import gdal
import rasterio as rio
import json

def get_extents(filename):
    gdal.UseExceptions()
    myopts = gdal.InfoOptions(options = ['-json'], reportProj4=True)
    myinfo = gdal.Info(filename,options=myopts)
    corner_coordinates = myinfo.get('cornerCoordinates')
    return corner_coordinates

def get_proj4(filename):
    gdal.UseExceptions()
    myopts = gdal.InfoOptions(options = ['-json'], reportProj4=True)
    myinfo = gdal.Info(filename,options=myopts)
    proj4 = myinfo.get('coordinateSystem').get('proj4')
    return proj4

def get_wkt(filename):
    gdal.UseExceptions()
    myopts = gdal.InfoOptions(options = ['-json'])
    myinfo = gdal.Info(filename,options=myopts)
    wkt = myinfo.get('coordinateSystem').get('wkt')
    return wkt

def get_nx_ny(filename):
    gdal.UseExceptions()
    myopts = gdal.InfoOptions(options = ['-json'], reportProj4=True)
    myinfo = gdal.Info(filename,options=myopts)
    (nx, ny) = myjson['size']
    (nx,ny) = myinfo.get('coordinateSystem').get('size')
    return (nx, ny)

def gdalwarp(src_file, dst_file, src_proj4, dst_proj4, nx, ny, xll, yll, xur, yur, output_type, resample_algorithm):

    gdal.UseExceptions()
    warp_options = gdal.WarpOptions(dstSRS=dst_proj4, 
                                    srcSRS=src_proj4,
                                    outputBounds=(xll,yll,xur,yur),
                                    width=nx,
                                    height=ny,
                                    outputBoundsSRS=dst_proj4,
                                    setColorInterpretation=True,
                                    outputType=output_type,
                                    resampleAlg=resample_algorithm)

    res = gdal.Warp(destNameOrDestDS=dst_file,
                    srcDSOrSrcDSTab=src_file,
                    options=warp_options)
    res = None

def gdal_translate( dst_file, src_file='temp.img', output_type=gdal.GDT_Float32, gdal_format='AAIGrid',nodata=-9999.):
    if output_type == gdal.GDT_Float32:
      translate_options = gdal.TranslateOptions(format=gdal_format, 
                                                outputType=output_type,
                                                creationOptions=["SIGNIFICANT_DIGITS=5"],
                                                noData=nodata)
    else:
      translate_options = gdal.TranslateOptions(format=gdal_format, 
                                                outputType=output_type,
                                                noData=nodata)
    
    res=gdal.Translate(dst_file,src_file,options=translate_options)
    res=None

def gdal_rasterize( dst_file, src_file, dst_proj4, resolution, xll, yll, xur, yur,
                    layer='', attribute='', gdal_format='HFA',
                    output_type=gdal.GDT_Float32, nodata=-9999):

    gdal.UseExceptions()
    rasterize_options = gdal.RasterizeOptions(
                              outputSRS=dst_proj4,
                              format=gdal_format,
                              outputType=output_type,
                              outputBounds=(xll,yll,xur,yur),
                              initValues=0,
                              xRes=resolution,
                              yRes=resolution,
                              attribute=attribute)
    res=gdal.Rasterize( dst_file,
                        src_file,
                        options=rasterize_options)
    res=None
