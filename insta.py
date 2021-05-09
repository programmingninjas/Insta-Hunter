import instaloader
import shutil
import os
from PIL import Image,ImageChops
from image_tools.sizes import resize_and_crop

def get_black_pixels(image):
    black_and_white_version = image.convert('1')
    black_pixels = black_and_white_version.histogram()[0]
    return black_pixels

def img_comp(current, expected):

        diff = ImageChops.difference(current, expected)
        black_pixels = get_black_pixels(diff)
        total_pixels = diff.size[0] * diff.size[1]
        similarity_ratio = black_pixels / total_pixels
        result = (1 - similarity_ratio) * 100
        print('The images are different by {}%'.format(result))
        return result


bot = instaloader.Instaloader()

bot.login('your username', 'your password')      #Need to login in Insta

user = input("Enter Username To Hunt: ")

profile = instaloader.Profile.from_username(bot.context, user)

path = input("Enter Image Relative Path: ")            #Like : programmingninjas.jpg

#To Convert png to jpg

if path.endswith('.png'):
    
    image = Image.open(path)
    image = image.convert('RGB')
    image.save(path.replace('.png','.jpg'))
    path = input("Enter Image Name Only: ") + '.jpg'

image1 = Image.open(path)                 

usernames = []

for i in profile.get_followers():

    usernames.append(i.username)

flag = True

for username in usernames:

    bot.download_profile(username,profile_pic_only = True)
    file_paths = [x for x in os.listdir(username)]
    image2 =  Image.open(username+'/'+file_paths[0])
    if flag:               #resizing image to improve algorithm #Optional
        img_to_resize = resize_and_crop(path, (image2.size[0],image2.size[1]), "middle")
        img_to_resize.save('resized_img.jpg')
        image1 = Image.open('resized_img.jpg')
    if  img_comp(image1,image2) < 10:
        print('\n')
        print("The Person Is: ",username)
        break
    else:
        image2.close()
        shutil.rmtree(username)
        flag = False
    
        




