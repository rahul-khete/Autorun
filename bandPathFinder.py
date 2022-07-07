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


