
def dataDown():
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


####################################################################################

def findPath():
    file=glob.glob("*.zip")
    with zipfile.ZipFile(file[0], 'r') as zip_ref:
            zip_ref.extractall()
    os.remove(file[0])

    bands=[]
    for root, dirs, files in os.walk("."):
        for f in files:
            s=os.path.relpath(os.path.join(root, f), ".")
            if s.find('R10m')!=-1 or s.find('R20m')!=-1:
                if s.find('B02')!=-1 and s.find('R10m')!=-1:
                    bands.append(s)
                if s.find('B03')!=-1 and s.find('R10m')!=-1:
                    bands.append(s)
                if s.find('B04')!=-1 and s.find('R10m')!=-1:
                    bands.append(s)
                if s.find('B08')!=-1 and s.find('R10m')!=-1:
                    bands.append(s)
                if s.find('B05')!=-1 and s.find('R20m')!=-1:
                  bands.append(s)
                if s.find('B11')!=-1 and s.find('R20m')!=-1:
                    bands.append(s)

    b2 = rio.open(bands[0])
    b3 = rio.open(bands[1])
    b4 = rio.open(bands[2])
    b8 = rio.open(bands[3])
    b5 = rio.open(bands[4])
    b11 = rio.open(bands[5])

    meta = b4.meta
    meta.update(driver='GTiff')
    meta.update(dtype=rio.float32)

    name=bands[0].split('_')[2][4:8]
    name=name[2:]+name[:2]
    if not os.path.exists('TIF_'+name):
        os.mkdir('TIF_'+name)

    path='./TIF_'+name+'/'

    return b2,b3,b4,b8,b11,meta,path


###############################################################

def ndviValue(b4,b8,path,meta):
    red=b4.read()
    nir=b8.read()
    ndvi = (nir.astype(float)-red.astype(float))/(nir+red)
    with rio.open(path+'NDVI.tif', 'w', **meta) as dst:
        dst.write(ndvi.astype(rio.float32))


    ndvi = rxr.open_rasterio(path+"NDVI.tif",
                                     masked=True).squeeze()

    #f, ax = plt.subplots(figsize=(10, 5))
    #ndvi.plot.imshow()
    #ax.set(title="NDVI")

    #ax.set_axis_off()
    #plt.show()

    shp = os.path.join('PalmTreeSite.shp')

    # Open crop extent (your study area extent boundary)
    crop_extent = geopandas.read_file(shp)
    #crop_extent = crop_extent.set_crs(4326, allow_override=True)
    ndvi_clipped = ndvi.rio.clip(crop_extent.geometry.apply(mapping),
                                          # This is needed if your GDF is in a diff CRS than the raster data
                                          crop_extent.crs)

    f, ax = plt.subplots(figsize=(10, 4))
    ndvi_clipped.plot(ax=ax)
    ax.set(title="Raster Layer Cropped to Geodataframe Extent")
    ax.set_axis_off()
    plt.show()

    pd.DataFrame(ndvi_clipped.values).head()

    ndvi_value=ndvi_clipped.mean()
    b4.close()
    b8.close()
    return ndvi_value

####################################################################################################


