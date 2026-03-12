import os
i = 5
for file in os.listdir(os.path.join("assets","Tiles","Batiment")):
    print(file,i)
    i += 1
# zone = [64,32]
# zone = zone[0] % 8, zone[1] % 8
# print (zone)