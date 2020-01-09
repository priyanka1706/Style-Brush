from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import cv2
import os
import shutil
from run_all_models import run_all
from test import ESR_gan
import os.path as osp
import glob
import cv2
import numpy as np
import torch
import RRDBNet_arch as arch


#orig1.jpeg lady with hat
#orig2.jpeg scenery
#orig3.jpg food
#orig4.jpg dog
#orig5.jpg eiffel tower
#orig6.jpg city

sets = "cam_formal"
orig = "orig.jpg"

class Region_Coords(object):

    DEFAULT_COLOR = 'black'
    File="images/content-images/"+orig
    arr=[]
    curr_image=[1]

    def __init__(self):
        self.root = Tk()
        
        #self.File = "orig.jpeg" #"C:/Users/Priyanka C/AnacondaProjects/CMPT 726 Project/orig.jpeg"
        self.img = ImageTk.PhotoImage(Image.open(self.File))
        
        self.first_style = Button(self.root, text='horses', command=self.use_style_one)
        self.first_style.grid(row=0, column=0, padx=0, pady=0)
        
        self.second_style = Button(self.root, text='trees', command=self.use_style_two)
        self.second_style.grid(row=0, column=1)
        
        self.third_style = Button(self.root, text='blue trees', command=self.use_style_three)
        self.third_style.grid(row=0, column=2)
        
        self.fourth_style = Button(self.root, text='sick child', command=self.use_style_four)
        self.fourth_style.grid(row=0, column=3)
        
        self.fifth_style = Button(self.root, text='candy', command=self.use_style_five)
        self.fifth_style.grid(row=0, column=4)
        
        self.sixth_style = Button(self.root, text='mosaic', command=self.use_style_six)
        self.sixth_style.grid(row=0, column=5)
        
        self.seventh_style = Button(self.root, text='udnie', command=self.use_style_seven)
        self.seventh_style.grid(row=0, column=6)
        
        self.eighth_style = Button(self.root, text='rain princess', command=self.use_style_eight)
        self.eighth_style.grid(row=0, column=7)
        
        self.c = Canvas(self.root, bg='white', width=self.img.width(), height=self.img.height())
        self.c.grid(row=1, columnspan=8)
        self.c.create_image(0,0,image=self.img,anchor="nw")
        
        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.eraser_on = False
        self.active_button = self.first_style
        self.activate_button(self.first_style, "images/output-images/"+sets+"/1-horses.jpg")
        self.style = "images/output-images/"+sets+"/1-horses.jpg"
        self.c.bind('<B1-Motion>', self.brushybrushy)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def use_style_one(self):
        self.activate_button(self.first_style, "images/output-images/"+sets+"/1-horses.jpg")

    def use_style_two(self):
        self.activate_button(self.second_style, "images/output-images/"+sets+"/2-trees.jpg")

    def use_style_three(self):
        self.activate_button(self.third_style, "images/output-images/"+sets+"/3-blue_trees.jpg")

    def use_style_four(self):
        self.activate_button(self.fourth_style, "images/output-images/"+sets+"/4-sick_child.jpg")

    def use_style_five(self):
        self.activate_button(self.fifth_style, "images/output-images/"+sets+"/5-candy.jpg")

    def use_style_six(self):
        self.activate_button(self.sixth_style, "images/output-images/"+sets+"/6-mosaic.jpg")

    def use_style_seven(self):
        self.activate_button(self.seventh_style, "images/output-images/"+sets+"/7-udnie.jpg")

    def use_style_eight(self):
        self.activate_button(self.eighth_style, "images/output-images/"+sets+"/8-rain_princess.jpg")
        
    def activate_button(self, some_button, curr_style):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.style = curr_style
        
    def brushybrushy(self, event):
        #self.c.create_line(0, 0, 30, 30, width=5.0, fill='blue', capstyle=ROUND, smooth=TRUE, splinesteps=36)
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=3, fill=self.DEFAULT_COLOR,
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y
        self.arr.append([event.x, event.y])
        self.curr_image.append(self.style)
        #print(self.arr)
        #print("")

    def reset(self, event):
        self.old_x, self.old_y = None, None
        self.arr=[]
        self.curr_image=[]
        print("stop")    

def free_form_roi(ip, roi_corners):
    image = cv2.imread(ip, -1)
    mask = np.zeros(image.shape, dtype=np.uint8)
    channel_count = image.shape[2]  
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    return image, mask

def save_mask(image, mask, style):
    #image_not = cv2.bitwise_not(image) #or image from where we want to get that roi
    #cv2.imwrite(style, image_not)
    d1 = 25 #int(image.shape[0]/7)
    d2 = 25 #int(image.shape[1]/10)
    if d1%2==0: d1+=1
    if d2%2==0: d2+=1
    cv2.GaussianBlur(mask, (d1, d2), 111, dst=mask)
    cv2.imwrite("images/output-images/"+sets+"/mask.jpg", mask)

def combine_pil(ip, style):
    src1 = np.array(Image.open(ip))
    src2 = np.array(Image.open(style).resize(src1.shape[1::-1], Image.BILINEAR))
    mask1 = np.array(Image.open("images/output-images/"+sets+"/mask.jpg").resize(src1.shape[1::-1], Image.BILINEAR))
    mask1 = mask1 / 255
    dst = src2 * mask1 + src1 * (1 - mask1)
    Image.fromarray(dst.astype(np.uint8)).save("images/output-images/"+sets+"/final.jpg")
    dst = cv2.imread("images/output-images/"+sets+"/final.jpg")
    cv2.imshow("Final", dst)
    cv2.waitKey()
    cv2.destroyAllWindows()

def get_cam_image():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    img_counter = 0
    while True:
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        if not ret:
            break
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            img_name = "images/content-images/orig.jpg"
            cv2.imwrite(img_name, frame)
            print("written!".format(img_name))
            img_counter += 1
            break
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    
    #Comment next line out to not run model
    get_cam_image()
    run_all(orig, sets)
    
    again = "y"
    prog_run = 1
    while again=="y" or again=="Y":
        Region_Coords()
        #print("From main",Region_Coords.arr)
    
        style = Region_Coords.curr_image
        #print("From main", style)
        style = style[len(style)-1]
        
        coord = Region_Coords.arr
        coord=np.array([coord])
        coord[:,[0,1]]=coord[:,[1,0]]
    
        if prog_run==1:
            ip = "images/content-images/"+orig
        else:
            ip = "images/output-images/"+sets+"/final.jpg"
        image, mask = free_form_roi(ip, coord)
        #combine(image, mask)
        
        save_mask(image, mask, style)
        combine_pil(ip, style)

        again = input("Do you want to run it again? y/n ")
        Region_Coords.arr=[]
        Region_Coords.style=[]
        Region_Coords.File="images/output-images/"+sets+"/final.jpg"
        prog_run+=1

    if not os.path.exists('images/output-images/'+sets+'/final'):
        os.mkdir('images/output-images/'+sets+'/final')
    
    shutil.move("images/output-images/"+sets+"/final.jpg", 'images/output-images/'+sets+'/final/final.jpg')

    ESR_gan(sets)

    print("THANK YOU")
