import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
import folium
coordinates = [(74.882083,17.057028), (74.882472,17.056917), (74.882444,17.056722), (74.882028,17.056833),(74.882083,17.057028)]
def create_polygon(coords, polygon_name):
  """ Create a polygon from coordinates"""
  polygon = Polygon(coords)
  gdf = gpd.GeoDataFrame(crs = {'init' :'epsg:4326'})
  gdf.loc[0,'name'] = polygon_name
  gdf.loc[0, 'geometry'] = polygon
  return gdf
shapefile = create_polygon(coordinates, 'abc')
# Export to shapefile if you want
shapefile.to_file("NewShape.shp")