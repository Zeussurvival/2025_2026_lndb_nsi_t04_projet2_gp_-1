import os
import numpy
# i = 5
# for file in os.listdir(os.path.join("assets","Tiles","Batiment")):
#     print(file,i)
#     i += 1
# zone = [64,32]
# zone = zone[0] % 8, zone[1] % 8
# print (zone)
matrice = numpy.full((10,10), 1,dtype=numpy.float32)
center = 5,5
range_depo = 4
to_remove = 0.1

def to_remove_bro(center,range_depo,to_remove):
    actuel = 0
    nb_a_faire = 1
    pos_actu = center
    for i in range(range_depo):
        if i == 0:
            matrice[center[0],center[1]] -= to_remove
        else:
            pos_actu=center[0]-i,center[1]-i
            for t in range(nb_a_faire+2*i):
                matrice[pos_actu[0],pos_actu[1]+t] -= to_remove
                matrice[pos_actu[0]+2*i,pos_actu[1]+t] -= to_remove
                actuel += 2*to_remove
            pos_actu=center[0]-i+1,center[1]-i
            for t in range(nb_a_faire+2*i-2):
                matrice[pos_actu[0]+t,pos_actu[1]] -= to_remove
                matrice[pos_actu[0]+t,pos_actu[1]+2*i] -= to_remove
                actuel += 2*to_remove
    return round(actuel,10)


print(to_remove_bro(center,range_depo,to_remove))
print(matrice)