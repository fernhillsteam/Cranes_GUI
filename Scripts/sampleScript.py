import tkinter
import tkinter.font as TkFont
import time
import math
import numpy as np
from shapely.geometry import LineString
from shapely.geometry import Point

#angle created by crane to another anchor/hoist < 


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
MAP_WIDTH = SCREEN_WIDTH
MAP_HEIGHT = SCREEN_HEIGHT
TOWER_CRANE_ANCHOR_RADIUS = 10
TOWER_CRANE_HOIST_RADIUS = 18
MOBILE_CRANE_ANCHOR_RADIUS = 10
MOBILE_CRANE_HOIST_RADIUS = 18

DANGER_ANGLE = 10

def create_animation_window():
    Window = tkinter.Tk()
    Window.title("Crane Monitor")
    Window.geometry(f'{SCREEN_WIDTH}x{SCREEN_HEIGHT}')
    return Window

def create_animation_canvas(Window):
    canvas = tkinter.Canvas(Window)
    canvas.configure(bg="White")
    canvas.pack(fill="both", expand=True)
    return canvas
Animation_Window = create_animation_window()
Animation_Canvas = create_animation_canvas(Animation_Window)

class TextInTheCircle():
    def __init__(self, name, centerX, centerY, radius, color, degree):
        self.name = name
        self.centerX = centerX
        self.centerY = centerY
        self.radius = radius
        self.color = color
        self.degree = degree

        self.circle = Animation_Canvas.create_oval(self.centerX - self.radius,
                                        self.centerY - self.radius,
                                        self.centerX + self.radius,
                                        self.centerY + self.radius,
                                        fill=self.color, outline="Black", width=1)
        #https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/create_text.html

        self.degree_text = Animation_Canvas.create_text(self.centerX,
                                                self.centerY,
                                                text = str(self.degree),
                                                #anchor=tkinter.CENTER,
                                                fill = "White",
                                                font = TkFont.Font(size = 25, weight = "bold")
                                                )
        if (self.name == "left"):
            textS = "Nearby left\nboom angle",
        elif (self.name == "right"):
            textS = "Nearby right\nboom angle",
        else:
            textS = "Nearby\nboom angle",
        self.textBelow = Animation_Canvas.create_text(self.centerX,
                                                self.centerY + self.radius * 1.8,
                                                text = textS,
                                                anchor=tkinter.CENTER,
                                                
                                                fill = "Black",
                                                font = TkFont.Font(size = 12, weight = "bold")
                                                )
    def updateText(self):
       
        Animation_Canvas.itemconfigure(self.degree_text,
                                                
                                                text = str(self.degree)
                                              
                                                )

class TowerCrane():
    def __init__(self, name = "", own = False, lat_anchor = 0, long_anchor = 0, alt_anchor = 0, lat_hoist = 0, long_hoist = 0, alt_hoist = 0, boom_length = 0):
        self.name = name
        self.own = own #being in this crane or not
        self.lat_anchor = lat_anchor
        self.long_anchor = long_anchor
        self.alt_anchor = alt_anchor

        self.lat_hoist = lat_hoist
        self.long_hoist = long_hoist
        self.alt_hoist = alt_hoist

        self.collide_anchor = False
        self.collide_hoist = False
        
        self.boom_length = boom_length
        
        self.anchor = Animation_Canvas.create_oval(lat_anchor - TOWER_CRANE_ANCHOR_RADIUS,
                                        long_anchor - TOWER_CRANE_ANCHOR_RADIUS,
                                        lat_anchor + TOWER_CRANE_ANCHOR_RADIUS,
                                        long_anchor + TOWER_CRANE_ANCHOR_RADIUS,
                                        fill="Black", outline="Black", width=1)
        print(self.anchor)
        self.hoist = Animation_Canvas.create_oval(lat_hoist - TOWER_CRANE_HOIST_RADIUS,
                                        long_hoist - TOWER_CRANE_HOIST_RADIUS,
                                        lat_hoist + TOWER_CRANE_HOIST_RADIUS,
                                        long_hoist + TOWER_CRANE_HOIST_RADIUS,
                                        fill="Green", outline="Black", width=1)
        print(self.hoist)
        self.boomAngle = math.atan2(self.long_hoist - self.long_anchor, self.lat_hoist - self.lat_anchor)
        if (self.own == True):
            self.boomColor = "Red"
        else:
            self.boomColor = "Green"
        self.boom = Animation_Canvas.create_line(lat_anchor, 
                                                long_anchor,
                                                lat_anchor + math.cos(self.boomAngle) *  self.boom_length,
                                                long_anchor + math.sin(self.boomAngle) * self.boom_length,
                                                width = 2, fill = self.boomColor

                                        )
        self.hoist_alt = Animation_Canvas.create_text(self.lat_hoist,
                                                self.long_hoist,
                                                text = str(self.alt_hoist),
                                                #anchor=tkinter.CENTER,
                                                fill = "White",
                                                font = TkFont.Font(size = 15, weight = "bold")
                                                )
        if (self.own == True):
            self.centerCircle = Animation_Canvas.create_oval(lat_anchor - self.boom_length,
                                        long_anchor - self.boom_length,
                                        lat_anchor + self.boom_length,
                                        long_anchor + self.boom_length,
                                        dash = (1,2),
                                        outline="Black", width=1)
        Animation_Canvas.tag_raise(self.hoist)
        Animation_Canvas.tag_raise(self.anchor)
        Animation_Canvas.tag_raise(self.hoist_alt)
    def updateTowerCrane(self,lat_anchor, long_anchor, alt_anchor, lat_hoist, long_hoist, alt_hoist):
        self.lat_anchor = lat_anchor
        self.long_anchor = long_anchor
        self.alt_anchor = alt_anchor

        self.lat_hoist = lat_hoist
        self.long_hoist = long_hoist
        self.alt_hoist = alt_hoist

        self.boomAngle = math.atan2(self.long_hoist - self.long_anchor, self.lat_hoist - self.lat_anchor)
        #print(math.degrees(self.boomAngle))
        Animation_Canvas.coords(self.anchor,
                                        self.lat_anchor - TOWER_CRANE_ANCHOR_RADIUS,
                                        self.long_anchor - TOWER_CRANE_ANCHOR_RADIUS,
                                        self.lat_anchor + TOWER_CRANE_ANCHOR_RADIUS,
                                        self.long_anchor + TOWER_CRANE_ANCHOR_RADIUS)
        Animation_Canvas.coords(self.hoist,
                                        self.lat_hoist - TOWER_CRANE_HOIST_RADIUS,
                                        self.long_hoist - TOWER_CRANE_HOIST_RADIUS,
                                        self.lat_hoist + TOWER_CRANE_HOIST_RADIUS,
                                        self.long_hoist + TOWER_CRANE_HOIST_RADIUS)
        Animation_Canvas.coords(self.boom,
                                    self.lat_anchor,
                                    self.long_anchor,
                                    lat_anchor + math.cos(self.boomAngle) *  self.boom_length,
                                    long_anchor + math.sin(self.boomAngle) * self.boom_length)
        
        if (self.collide_hoist == True):
            Animation_Canvas.itemconfigure(self.hoist, fill = "Red")
        else:
            Animation_Canvas.itemconfigure(self.hoist, fill = "Green")
class MobileCrane():
    def __init__(self, name = "", own = False, lat_anchor = 0, long_anchor = 0, alt_anchor = 0, lat_hoist = 0, long_hoist = 0, alt_hoist = 0):
        self.name = name
        self.own = own
        self.lat_anchor = lat_anchor
        self.long_anchor = long_anchor
        self.alt_anchor = alt_anchor

        self.lat_hoist = lat_hoist
        self.long_hoist = long_hoist
        self.alt_hoist = alt_hoist
        
        self.collide_anchor = False
        self.collide_hoist = False
        
        self.anchor = Animation_Canvas.create_oval(lat_anchor - MOBILE_CRANE_ANCHOR_RADIUS,
                                        long_anchor - MOBILE_CRANE_ANCHOR_RADIUS,
                                        lat_anchor + MOBILE_CRANE_ANCHOR_RADIUS,
                                        long_anchor + MOBILE_CRANE_ANCHOR_RADIUS,
                                        fill="Black", outline="Black", width=1)
        print(self.anchor)
        self.hoist = Animation_Canvas.create_oval(lat_hoist - MOBILE_CRANE_HOIST_RADIUS,
                                        long_hoist - MOBILE_CRANE_HOIST_RADIUS,
                                        lat_hoist + MOBILE_CRANE_HOIST_RADIUS,
                                        long_hoist + MOBILE_CRANE_HOIST_RADIUS,
                                        fill="Yellow", outline="Black", width=1)
        print(self.hoist)
        self.boomAngle = math.atan2(self.long_hoist - self.long_anchor, self.lat_hoist - self.lat_anchor)
        if (self.own == True):
            self.boomColor = "Red"
        else:
            self.boomColor = "Green"
        self.boom_length = math.sqrt(math.pow(self.lat_hoist-self.lat_anchor,2)+ math.pow(self.long_hoist-self.long_anchor,2) )
        self.boom = Animation_Canvas.create_line(lat_anchor, 
                                                long_anchor,
                                                lat_hoist,
                                                long_hoist,
                                                width = 2, fill = self.boomColor

                                        )
        self.hoist_alt = Animation_Canvas.create_text(self.lat_hoist,
                                                self.long_hoist,
                                                text = str(self.alt_hoist),
                                                #anchor=tkinter.CENTER,
                                                fill = "White",
                                                font = TkFont.Font(size = 15, weight = "bold")
                                                )
        Animation_Canvas.tag_raise(self.hoist)
        Animation_Canvas.tag_raise(self.anchor)
        Animation_Canvas.tag_raise(self.hoist_alt)
    def updateMobileCrane(self,lat_anchor, long_anchor, alt_anchor, lat_hoist, long_hoist, alt_hoist):
        self.lat_anchor = lat_anchor
        self.long_anchor = long_anchor
        self.alt_anchor = alt_anchor

        self.lat_hoist = lat_hoist
        self.long_hoist = long_hoist
        self.alt_hoist = alt_hoist

        self.boomAngle = math.atan2(self.long_hoist - self.long_anchor, self.lat_hoist - self.lat_anchor)
        #print(math.degrees(self.boomAngle))
        Animation_Canvas.coords(self.anchor,
                                        self.lat_anchor - MOBILE_CRANE_ANCHOR_RADIUS,
                                        self.long_anchor - MOBILE_CRANE_ANCHOR_RADIUS,
                                        self.lat_anchor + MOBILE_CRANE_ANCHOR_RADIUS,
                                        self.long_anchor + MOBILE_CRANE_ANCHOR_RADIUS)
        Animation_Canvas.coords(self.hoist,
                                        self.lat_hoist - MOBILE_CRANE_HOIST_RADIUS,
                                        self.long_hoist - MOBILE_CRANE_HOIST_RADIUS,
                                        self.lat_hoist + MOBILE_CRANE_HOIST_RADIUS,
                                        self.long_hoist + MOBILE_CRANE_HOIST_RADIUS)
        Animation_Canvas.coords(self.boom,
                                    self.lat_anchor,
                                    self.long_anchor,
                                    self.lat_hoist,
                                    self.long_hoist)
        if (self.collide_hoist == True):
            Animation_Canvas.itemconfigure(self.hoist, fill = "Red")
        else:
            Animation_Canvas.itemconfigure(self.hoist, fill = "Green")


tw1 = TowerCrane("TW1", True, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 0, SCREEN_WIDTH/2 , SCREEN_HEIGHT/2 - 20, 100, 200)
mb1 = MobileCrane("MB1", False, 200, 300, 0, 300, 250, 10)
mb2 = MobileCrane("MB2", False, 700, 400, 0, 700, 300, 20)
left_boom_angle = TextInTheCircle("left",80,50,40,"Green",10)
right_boom_angle = TextInTheCircle("right",SCREEN_WIDTH - 80,50,40,"Green",10)
while True:
    #Animation_Window.update()
    #tw1.lat_hoist = tw1.lat_hoist - 10
    #tw1.long_hoist = tw1.long_hoist + 10
    #print(tw1.lat_hoist, tw1.long_hoist)


    #calcualting angle
    """
    vector_1 = [0, 1]
    vector_2 = [1, 0]

    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)

    
    p = Point(5,5)
    c = p.buffer(3).boundary
    l = LineString([(0,0), (10, 10)])
    i = c.intersection(l)

    print(i.geoms[0].coords[0])
    #(2.8786796564403576, 2.8786796564403576)
    """

    p = Point(tw1.lat_anchor,tw1.long_anchor)
    c = p.buffer(tw1.boom_length).boundary
    l = LineString([(tw1.lat_anchor,tw1.long_anchor), (tw1.lat_hoist * 1.5,tw1.long_hoist * 1.5)])
    i = c.intersection(l)
    print(i)

    tw1.updateTowerCrane(tw1.lat_anchor,tw1.long_anchor, tw1.alt_anchor, tw1.lat_hoist, tw1.long_hoist, tw1.alt_hoist)
    mb1.updateMobileCrane(mb1.lat_anchor,mb1.long_anchor, mb1.alt_anchor, mb1.lat_hoist, mb1.long_hoist, mb1.alt_hoist)
    mb2.updateMobileCrane(mb2.lat_anchor,mb2.long_anchor, mb2.alt_anchor, mb2.lat_hoist, mb2.long_hoist, mb2.alt_hoist)
    right_boom_angle.degree = 20
    right_boom_angle.updateText()

    for i in range(100,200):
        for j in range(100,300):
            tw1.updateTowerCrane(tw1.lat_anchor,tw1.long_anchor, tw1.alt_anchor, tw1.lat_hoist, tw1.long_hoist, tw1.alt_hoist)
            mb1.updateMobileCrane(mb1.lat_anchor,mb1.long_anchor, mb1.alt_anchor, i, j, mb1.alt_hoist)
            mb2.updateMobileCrane(mb2.lat_anchor,mb2.long_anchor, mb2.alt_anchor, mb2.lat_hoist, mb2.long_hoist, mb2.alt_hoist)
            right_boom_angle.degree = 20
            right_boom_angle.updateText()
            Animation_Window.update()
            #time.sleep(0.1)

    time.sleep(0.1)
    Animation_Window.update()
   
        
