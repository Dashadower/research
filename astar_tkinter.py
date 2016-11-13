import tkinter
from tkinter.constants import *




class AStarExample(tkinter.Frame):
    def __init__(self,parent,start=(5,5),end=(9,5),size=20,walls=[]):
        self.parent = parent
        self.startpoint = start
        self.endpoint = end
        self.size = size
        self.tilesize = 50
        self.f = {}
        self.g = {}
        self.h = {}
        self.open = []
        self.closed = []
        self.walls = walls
        self.stop = False
        self.path = []
        self.written = []
        tkinter.Frame.__init__(self,self.parent)
        self.pack(fill=BOTH,expand=YES)


        self.x = tkinter.IntVar()
        self.x.set(0)
        self.y = tkinter.IntVar()
        self.y.set(0)

        self.display = tkinter.Canvas(self,bg="black")
        self.display.pack(expand=YES,fill=BOTH)
        self.parent.bind("<MouseWheel>", self.mouse_wheel)
        self.parent.bind("<ButtonPress-1>", self.scroll_start)
        self.parent.bind("<B1-Motion>", self.scroll_move)

        self.makedisplay()
    def mouse_wheel(self,event):

        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            self.display.scale("all",self.x.get(),self.y.get(),0.9,0.9)
        if event.num == 4 or event.delta == 120:
            self.display.scale("all",self.x.get(),self.y.get(),1.1,1.1)

    def scroll_start(self,event):
        self.display.scan_mark(event.x, event.y)
    def scroll_move(self,event):
        self.display.scan_dragto(event.x, event.y, gain=1)

    def makedisplay(self):
        for x_con in range(0,self.size+1):
            for y_con in range(0,self.size+1):
                self.display.create_rectangle(x_con*self.tilesize,y_con*self.tilesize,(x_con*self.tilesize)+self.tilesize,(y_con*self.tilesize)+self.tilesize,outline="blue")
        for items in self.walls:
            self.display.create_rectangle(items[0]*self.tilesize,items[1]*self.tilesize,(items[0]*self.tilesize)+self.tilesize,(items[1]*self.tilesize)+self.tilesize,fill="grey")
        self.display.create_rectangle(self.startpoint[0]*self.tilesize,self.startpoint[1]*self.tilesize,self.startpoint[0]*self.tilesize+self.tilesize,self.startpoint[1]*self.tilesize+self.tilesize,fill="green")
        self.display.create_rectangle(self.endpoint[0]*self.tilesize,self.endpoint[1]*self.tilesize,self.endpoint[0]*self.tilesize+self.tilesize,self.endpoint[1]*self.tilesize+self.tilesize,fill="red")
    def start(self):
        self.closed.append(self.startpoint)
        self.g[str(self.startpoint)] = 0
        data = []
        for tiles in self.get_8(self.startpoint):
            self.open.append(tiles)
            if tiles in self.walls:
                self.open.remove(tiles)
                self.closed.append(tiles)
            else:
                f = self.calculate_score(self.startpoint,tiles)

                g = self.g[str(tiles)]
                h = self.h[str(tiles)]

                self.display.create_text(tiles[0]*self.tilesize,tiles[1]*self.tilesize,text=f,fill="white",font=("Segoe UI",8),anchor=NW)
                self.display.create_text(tiles[0]*self.tilesize,(tiles[1]*self.tilesize)+self.tilesize-8,text=g,fill="white",font=("Segoe UI",8),anchor=W)
                self.display.create_text((tiles[0]*self.tilesize)+self.tilesize,(tiles[1]*self.tilesize)+self.tilesize-8,text=h,fill="white",font=("Segoe UI",8),anchor=E)
                data.append((tiles,f))
        t2 =sorted(data,key=self.getkey)

        self.closed.append(t2[0][0])

        if t2[0][0] in self.open: self.open.remove(t2[0][0])

        self.choose_efficient(self.startpoint,t2[0][0])
        self.finished()
    def get_8(self,coord):
        data = []
        for x,y in [(coord[0]+i,coord[1]+j) for i in (-1,0,1) for j in (-1,0,1) if i != 0 or j != 0]:
            if x > self.size or x < 0 or y > self.size or y < 0:
                pass
            else: data.append((x,y))
        return data
    def calculate_score(self,master,coord):
        if master[0] == coord[0] or master[1] == coord[1]: type = "normal"
        else: type="diag"
        if type == "diag": g = self.g[str(master)] + 14
        else: g = self.g[str(master)] + 10

        h = abs(coord[0]-self.endpoint[0])*10+abs(coord[1]-self.endpoint[1])*10
        f = g + h
        self.h[str(coord)] = h
        self.g[str(coord)] = g
        self.f[str(coord)] = f
        return f
    def calculate_score_norecord(self,master,coord):
        if master[0] == coord[0] or master[1] == coord[1]: type = "normal"
        else: type="diag"
        if type == "diag": g = self.g[str(master)] + 14
        else: g = self.g[str(master)] + 10

        h = abs(coord[0]-self.endpoint[0])*10+abs(coord[1]-self.endpoint[1])*10
        f = g + h
        return (f,g,h)
    def getkey(self,item):
        return item[1]
    def get_corners(self,cor1,cor2):
        data = [(cor1[0],cor2[1]),(cor2[0],cor1[1])]
        flag = False
        for items in data:
            if items in self.walls:
                flag = True
                break
        return flag
    def finished(self):
        print("done")

        print("path:",self.path)
        self.path.insert(0,self.startpoint)
        self.path.insert(-1,self.endpoint)
        p1 = 1

        while p1 < len(self.path):

            self.display.create_line((self.path[p1-1][0]*self.tilesize)+self.tilesize/2,(self.path[p1-1][1]*self.tilesize)+self.tilesize/2,(self.path[p1][0]*self.tilesize)+self.tilesize/2,(self.path[p1][1]*self.tilesize)+self.tilesize/2,fill="red",width="10")
            p1 += 1

    def choose_efficient(self,parent,coord):
        print("parent:",parent,"current:",coord)
        data = []
        writable = []
        calc = []
        for tiles in self.get_8(coord):
            if tiles == self.endpoint:

                return self.path
            elif tiles in self.walls: pass
            elif tiles in self.closed:pass
            elif self.get_corners(coord,tiles) == True and tiles not in self.open:

                writable.append(tiles)

            else:
                writable.append(tiles)
                calc.append(tiles)
        for objects in writable:
            f = self.calculate_score(parent,objects)

            g = self.g[str(objects)]
            h = self.h[str(objects)]

            if objects not in self.written:
                self.display.create_text(objects[0]*self.tilesize,objects[1]*self.tilesize,text=f,fill="white",font=("Segoe UI",8),anchor=NW)
                self.display.create_text(objects[0]*self.tilesize,(objects[1]*self.tilesize)+self.tilesize-8,text=g,fill="white",font=("Segoe UI",8),anchor=W)
                self.display.create_text((objects[0]*self.tilesize)+self.tilesize,(objects[1]*self.tilesize)+self.tilesize-8,text=h,fill="white",font=("Segoe UI",8),anchor=E)
                self.written.append(objects)
        for dc in calc:
            if dc == self.endpoint:
                return self.path
            elif tiles in self.open:
                if self.g[str(tiles)] < self.calculate_score_norecord(parent,tiles)[1]:
                    self.closed.append(dc)
                    print(tiles)
                    if tiles in self.open: self.open.remove(dc)
                    else: pass



                    self.path.append(dc)
                    self.choose_efficient(parent,dc)
                else: data.append((dc,self.f[str(dc)]))
            else:
                self.open.append(dc)
                data.append((dc,self.f[str(dc)]))

        t2 =sorted(data,key=self.getkey)

        self.closed.append(t2[0][0])

        if t2[0][0] in self.open: self.open.remove(t2[0][0])
        self.path.append(t2[0][0])

        self.choose_efficient(coord,t2[0][0])






root = tkinter.Tk()
walls = [(1,19),(2,18),(3,17),(4,16),(5,15),(6,14),(7,13),(8,12),(9,11),(10,10),(11,9),(12,8),(13,7),(14,6),(15,5),(16,4),(17,3),(18,2),(19,1),(23,0),(22,1),(21,2),(20,3),(19,4),(18,5),(17,6),(16,7),(37,40),(38,39),(40,37),(40,35),(39,35)]
mystar = AStarExample(root,start=(0,0),end=(40,40),walls=walls,size=40)

mystar.start()
root.update()
root.mainloop()