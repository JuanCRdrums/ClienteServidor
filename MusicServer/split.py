import json
import os

files1 = []
files2 = []

def store(name,contents,n):
    list = name.split(".")
    newname = list[0] + str(n) + ".mp3"
    with open(newname,"ab") as f:
        f.write(contents)

#Fuente: mkyoung.com (hasta la línea 10)
for r,d,f in os.walk('Server1'):
    for file in f:
        files1.append(os.path.join(r, file))


for r,d,f in os.walk('Server2'):
    for file in f:
        files2.append(os.path.join(r, file))


js = {}

for f in files1:
    with open(f,"rb") as file:
        size = os.path.getsize(f)
        n = 1
        for i in range(0,size,500000):
            file.seek(i)
            contents = file.read(500000)
            store(f,contents,n)
            n += 1
        l = f.split("/")
        nameToStore = l[1]
        js[nameToStore] = [1,n]
    os.remove(f)

for f in files2:
    with open(f,"rb") as file:
        size = os.path.getsize(f)
        n = 1
        for i in range(0,size,500000):
            file.seek(i)
            contents = file.read(500000)
            store(f,contents,n)
            n += 1
        l = f.split("/")
        nameToStore = l[1]
        js[nameToStore] = [2,n]
    os.remove(f)

with open("Proxy/partes.json", "w") as fjson:
    #print(js)
    json.dump(js,fjson)
