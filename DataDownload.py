currentDate = datetime.date.today()
nextDate=currentDate.strftime("%Y%m%d")


nReserve = geopandas.read_file('PalmTreeSite.shp')

m2 = folium.Map([16.6231763,73.9119105], zoom_start=12)
folium.GeoJson(nReserve).add_to(m2)
# m2

footprint =None
for i in nReserve['geometry']:
    footprint = i
    

user = 'aniket.mane.1238' 
password = 'Aniket@1238' 
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')


products = api.query(footprint,
                     date = ('20220601', nextDate),
                     platformname = 'Sentinel-2',
                     processinglevel = 'Level-2A',
                     cloudcoverpercentage = (0,100)
                    )


products_gdf = api.to_geodataframe(products)

api.download(products_gdf['uuid'][0])
