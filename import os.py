import os
# for file in os.listdir(os.path.join("assets","Building_txt")):
#     print(file)
zone = [64,32]
zone = zone[0] % 8, zone[1] % 8
print (zone)