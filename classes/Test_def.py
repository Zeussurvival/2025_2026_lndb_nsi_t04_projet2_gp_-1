import numpy as np
import random
def place_matrice_big_then_small(matrice,house_matrice,positions):
    for true_y in range(house_matrice.shape[0]):
        for true_x in range(house_matrice.shape[1]):
            if 0 <= positions[1]+true_y < matrice.shape[1] and 0 <= positions[0]+true_x < matrice.shape[0]:
                matrice[positions[1]+true_y,positions[0]+true_x] = house_matrice[true_y,true_x]
    return matrice

def place_matrice_big_then_small_addition(matrice,house_matrice,positions):
    for true_y in range(house_matrice.shape[0]):
        for true_x in range(house_matrice.shape[1]):
            if 0 <= positions[1]+true_y < matrice.shape[0] and 0 <= positions[0]+true_x < matrice.shape[1]:
                matrice[positions[1]+true_y,positions[0]+true_x] += house_matrice[true_y,true_x]
    return matrice

def creation_map_rectangle(width,height,num):
    Map = np.full((width,height), num,dtype=np.int32)
    return Map

def create_round_matrice(radius):
    matrice = np.zeros((radius*2+1,radius*2+1))
    matrice[radius,radius] = 1
    matrice[radius,radius+2] = 1
    for x in range(matrice.shape[1]):
        distance_x = radius - x
        # print(distance_x)
        # print(matrice[x])
        for y in range(matrice.shape[0]):
            distance_y = radius - y
            num = min(max(0,1 - (distance_x**2+distance_y**2-1)/(radius**2)),1) #le - 1 permet davoir des contours avec quand meme une certaine valeur
            matrice[x,y]= num # et le min du dessus permet davoir le centre la valeur 1 assez forte
            # print(matrice[x,y])
    return matrice

def create_random_pos(seed,numbers_to_gen,map_length):
    random.seed(seed)
    map_total = map_length[0] * map_length[1]
    Liste_n = []
    for _ in range(numbers_to_gen):
        num = int(random.random()*map_total)
        Liste_n.append((num // map_length[0],num % map_length[0]))
    return Liste_n

def pollution_creation_rond(Liste_pos,range_pollu,map): # pas forcement realiste au top mais bon
    map_pollution = np.zeros(map.shape)
    for pos in Liste_pos:
        matrice_created = create_round_matrice(range_pollu)
        map_pollution = place_matrice_big_then_small_addition(map_pollution,matrice_created,(pos[0]-range_pollu,pos[1]-range_pollu)) # place_matrice_big_then_small(matrice,house_matrice,positions)
    # print(Liste_pos)
    # print(map_pollution)
    return map_pollution

 


# mat = create_round_matrice(5)
# for row in mat:
#     print(row)


def set_pollution_map_rectangle(number_of_pos,seed,map_actu,range_pollu):
    Liste_pos = create_random_pos(seed,number_of_pos,map_actu.shape) # generation positions pr pollution
    new_map = pollution_creation_rond(Liste_pos,range_pollu,map_actu) # creation de la vrai map de pollution
    # print(new_map)
    # print(Liste_pos)
    return new_map


def floor_pollution_map_at_smth(map,floor_num):
    for i in range(map.shape[0]):
        for y in range(map.shape[1]):
            if map[i,y] >floor_num:
                map[i,y] = floor_num
    return map

