from PIL import Image
import os
main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir,"assets")
temp_dir = os.path.join(assets_dir,"Tiles","Batiment") # main_dir # assets_dir,"Tiles","Batiment"
construction_dir = os.path.join(assets_dir,"Building_txt") # main_dir # assets_dir
test_map_dir = os.path.join(main_dir,"Test map json")
print(main_dir)



image = Image.open("Test map json/bat1.png").convert("RGBA")
print("Taille de l'image:", image.size)
print("Mode de couleur:", image.mode)
print("Format de l'image:", image.format)
size_image = image.size
Liste_des_tiles_de_limage = []

tiles_x = image.size[0] // 8
tiles_y = image.size[1] // 8

Liste_des_tiles_de_limage = []

for y in range(tiles_y):
    for x in range(tiles_x):
        changed = False
        zone = (x*8, y*8, x*8+8, y*8+8)
        image_coupee = image.crop(zone)

        for filename in os.listdir(temp_dir):
            path = os.path.join(temp_dir, filename)
            img_exist = Image.open(path).convert("RGBA")
            if image_coupee.tobytes() == img_exist.tobytes():
                Liste_des_tiles_de_limage.append(f"{filename}")
                changed = True
                break
        if not changed:
            nb_images = len(os.listdir(temp_dir))
            filename = f"{nb_images}_image.png"
            path = os.path.join(temp_dir, filename)

            image_coupee.save(path)
            Liste_des_tiles_de_limage.append(f"{filename}")
print(str(size_image[0]//8)+str(size_image[1]//8)+"\n")
print(Liste_des_tiles_de_limage)
with open(os.path.join(construction_dir,"constru_3.txt"),"w") as f:
    f.write(str(size_image[0]//8)+"\n")
    f.write(str(size_image[1]//8)+"\n")
    for txt in Liste_des_tiles_de_limage:
        f.write(txt+"\n")

# print(Image.open("Temp/4_image.png").convert("RGBA").tobytes()) # (96, 64, 104, 72)
# print(image.crop((96, 64, 104, 72)).tobytes())
print(image.crop((96,64,104,72)).getpixel((0,0)))
# print(Image.open("Temp/4_image.png").getpixel((0,0)))