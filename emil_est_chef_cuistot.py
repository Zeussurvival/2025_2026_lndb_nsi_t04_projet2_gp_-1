from PIL import Image
import os
main_dir = os.path.split(os.path.abspath(__file__))[0]
temp_dir = os.path.join(main_dir,"Temp")
test_map_dir = os.path.join(main_dir,"Test map json")
print(main_dir)



image = Image.open("Test map json/bat3.png").convert("RGBA")
print("Taille de l'image:", image.size)
print("Mode de couleur:", image.mode)
print("Format de l'image:", image.format)

Liste_des_tiles_de_limage = []

def donne_le_nombre_si_inf_ou_egale_sinon_modulo(nombre,modu_a):
    if nombre % modu_a == 0:
        return modu_a
    return nombre%modu_a


for i in range ((image.size[0]//8)*(image.size[1]//8)):
    changed = False
    zone = (8*i%image.size[0], 8*(8*i//image.size[0]), donne_le_nombre_si_inf_ou_egale_sinon_modulo(8*(i+1),(image.size[0])), 8+8*((8*i)//image.size[0]))
    print(zone)
    image_coupee = image.crop(zone)
    list_image = os.listdir(temp_dir)
    for A, filename in enumerate(os.listdir(temp_dir)):
        path = os.path.join(temp_dir, filename)
        img_exist = Image.open(path).convert("RGBA")

        if image_coupee.size == img_exist.size and \
        image_coupee.tobytes() == img_exist.tobytes():
            Liste_des_tiles_de_limage.append(f"Temp/{filename}")
            changed = True
            break
    print(changed,i)
    if not changed:
        text = "Temp/"+str(i)+"_image.png"
        Liste_des_tiles_de_limage.append("Temp/"+str(i)+"_image.png")
        image_coupee.save((text))


print(Liste_des_tiles_de_limage)
print((9*10)%19,(9*10)/19,(9*10)//19)
print(os.path.join(main_dir,"spritesheet.png"))

print(Image.open("Temp/4_image.png").convert("RGBA").tobytes()) # (96, 64, 104, 72)
print(image.crop((96, 64, 104, 72)).tobytes())
# img = Image.open(os.path.join(temp_dir,"36_image.png")).convert("RGBA")
# img.show()