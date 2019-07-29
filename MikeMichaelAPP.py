#  -*-coding:utf-8-*-

import os
import time
import pygame
import Tkinter
from Tkinter import *
from PIL import Image, ImageTk
from mutagen.mp3 import MP3

photo = []
button1 = None
button2 = None
button3 = None
button4 = None
mins = None
plus = None
pygame.mixer.init()

class Music(object):

    def PlayerInit(self):
        return pygame.mixer.music

    def GetPlayer(self):
        return pygame.mixer.music

    def GetMusicLength(self,filename):
        return MP3(filename).info.length

    def getKeybyItem(self, _dict, value):
        for index in _dict.keys():
            if _dict[index] == value:
                return index
        return 0

    def changeImage(self,count):
        global photo
        imagenum = count%len(photo)
        self.imageLabel.configure(image=photo[imagenum])
        count += 1
        self.imageLabel.after(2000, self.changeImage, count)

    def __init__(self):
        self.appGui = Tk()
        self.appGui.Color = "red"
        self.appGui.title("水晶音乐播放器V1.01 迈克尔制作")
        self.appGui.geometry("950x700+300+100")
        self.appGui.resizable(False, False)
        self.musicName = ""
        self.musiclist = {}
        self.index = 0
        self.size = 0
        self.length = 1000
        self.position = 0

    def quit(self):
        pygame.quit()
        self.appGui.quit()

    def __MusciList__(self):
        self.appMusicList = Frame(self.appGui, height=20, bd=20, bg="Gainsboro")
        self.titleLabel = Label(self.appMusicList, text="音乐播放列表", padx=4, pady=10, bg="Gainsboro")
        index = 0
        for root, dirs, filenames in os.walk("./"):
            for name in filenames:
                if name.find("mp3") >= 0:
                    self.musiclist[index] = name
                    index += 1
        self.musicTree = Listbox(self.appMusicList, bg="Gainsboro", height=len(self.musiclist), relief="flat", selectmode="browse")
        self.musicTree.bind("<Double-Button-1>",self.selectPlay)
        for key in self.musiclist:
            self.musicTree.insert(0, self.musiclist[key])
        self.size = len(self.musiclist.keys())
        self.quitbutton = Button(self.appMusicList, text="退出程序", command=self.quit, padx=8, pady=0, fg="gray", relief="sunken")

    def __MusicBackground__(self):
        global photo
        self.appMusicBackground = Frame(self.appGui, height=80, bd=20, bg="white")
        for root, dirs, filenames in os.walk("./resource/background/"):
            for filename in filenames:
                photo.append(ImageTk.PhotoImage(Image.open("./resource/background/%s"%str(filename))))
        self.imageLabel = Label(self.appMusicBackground, image=photo[0])



    def __MusicPerform__(self):
        global button1
        global button2
        global button3
        global button4
        button1 = ImageTk.PhotoImage(Image.open("./resource/button/prev.jpg"))
        button2 = ImageTk.PhotoImage(Image.open("./resource/button/play.jpg"))
        button3 = ImageTk.PhotoImage(Image.open("./resource/button/stop.jpg"))
        button4 = ImageTk.PhotoImage(Image.open("./resource/button/next.jpg"))
        self.prev = Button(self.appGui, command=self.prevMuisc, width=16, height=16, image=button1)
        self.next = Button(self.appGui, command=self.nextMuisc, width=16, height=16, image=button4)
        self.play = Button(self.appGui, command=self.playMuisc, width=16, height=16, image=button2)
        self.stop = Button(self.appGui, command=self.stopMuisc, width=16, height=16, image=button3)

    def __Music__(self):
        self.music = Label(self.appGui, text=self.musicName)
        self.canvas = Canvas(self.appGui, width=600, height=3, bg='darkgray')
        self.canvas.bind("<Button-1>", self.onMove)

    def __Voloum__(self):
        global mins
        global plus
        plus = ImageTk.PhotoImage(Image.open("./resource/button/plus.jpg"))
        mins = ImageTk.PhotoImage(Image.open("./resource/button/mins.jpg"))
        self.volume_plus = Button(self.appGui, command=self.volumePlus, width=8, height=8, image=plus)
        self.volume_mins = Button(self.appGui, command=self.volumeMins, width=8, height=8, image=mins)

    def onMove(self, event):
        position = float((float(event.x)/600)*self.length)
        self.playMuisc(position)


    def volumeMins(self):
        volume = pygame.mixer.music.get_volume() - 0.1
        volume = volume if volume > 0.0 else 0.0
        pygame.mixer.music.set_volume(volume)

    def volumePlus(self):
        volume = pygame.mixer.music.get_volume() + 0.1
        volume = volume if volume < 1.0 else 1.0
        pygame.mixer.music.set_volume(volume)

    def getStarted(self):
        global photo
        self.__MusciList__()
        self.__MusicBackground__()
        self.__Music__()
        self.__MusicPerform__()
        self.__Voloum__()
        self.appMusicList.pack(fill="y", side="left", padx=0, pady=0)
        self.titleLabel.pack()
        self.musicTree.pack(padx=0, pady=0)
        self.quitbutton.pack(side="bottom", padx=10, pady=20)
        self.appMusicBackground.pack(fill="x", side="top", padx=0, pady=0)
        self.imageLabel.pack(padx=0, pady=5)
        count = 1
        self.imageLabel.after(2000, self.changeImage, count)
        self.prev.place(x=420, y=600)
        self.play.place(x=520, y=600)
        self.stop.place(x=620, y=600)
        self.next.place(x=720, y=600)
        self.volume_plus.place(x=910, y=660)
        self.volume_mins.place(x=860, y=660)
        self.music.place(x=260, y=630)
        self.canvas.place(x=240,y=665)
        self.appGui.mainloop()

    def prevMuisc(self):
        fill = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="darkgray")
        self.canvas.coords(fill, (0, 0, 600, 100))
        self.appGui.update()
        self.index = self.getKeybyItem(self.musiclist, self.musicName)
        self.index = self.index - 1  if self.index > 0 else self.size-1
        self.musicName = self.musiclist[self.index]
        player = self.PlayerInit()
        self.music = Label(self.appGui, text=" "*120)
        self.music.place(x=260, y=630)
        self.music = Label(self.appGui, text=self.musicName[0:100])
        self.music.place(x=260, y=630)
        player.load("./music/%s"%str(self.musicName))
        self.length = self.GetMusicLength("./music/%s"%str(self.musicName))
        player.play()
        fill = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
        while((pygame.mixer.music.get_pos()/1000) < self.length):
            count = int(pygame.mixer.music.get_pos()/1000/self.length*600)
            self.canvas.coords(fill, (0, 0, count, 100))
            self.appGui.update()
            time.sleep(0.02)

    def playMuisc(self, starts=0):
        if self.position != 0:
            try:
                pygame.mixer.music.unpause()
            except Exception, reason:
                pass
        else:
            fill = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="darkgray")
            self.canvas.coords(fill, (0, 0, 600, 100))
            self.appGui.update()
            player = self.PlayerInit()
            if self.index >= 0:
                self.musicName = self.musiclist[self.index]
            else:
                self.musicName = self.musiclist[0]
            try:
                player.load("./music/%s"%str(self.musicName))
                self.music = Label(self.appGui, text=" "*120)
                self.music.place(x=260, y=630)
                self.music = Label(self.appGui, text=self.musicName[0:100])
                self.music.place(x=260, y=630)
            except Exception,reason:
                pass
            self.length = self.GetMusicLength("./music/%s"%str(self.musicName))
            pbit = True
        fill = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, outline="green", fill="green")
        if starts !=0:
            fill = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=int((float(starts)/self.length)*1230), outline="green", fill="green")
        if pbit:
            player.play(start=starts)
        try:
            while((pygame.mixer.music.get_pos()/1000) < self.length):
                count = int(pygame.mixer.music.get_pos()/1000/self.length*600)
                self.canvas.coords(fill, (0, 0, count, 100))
                self.appGui.update()
                time.sleep(0.02)
        except Exception, reason:
            pass

    def stopMuisc(self):
        self.GetPlayer().pause()
        self.position = pygame.mixer.music.get_pos()

    def nextMuisc(self):
        fill = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="darkgray")
        self.canvas.coords(fill, (0, 0, 600, 100))
        self.appGui.update()
        self.index = self.getKeybyItem(self.musiclist, self.musicName)
        self.index = self.index + 1  if self.index < self.size else 0
        self.musicName = self.musiclist[self.index]
        player = self.PlayerInit()
        self.music = Label(self.appGui, text=" "*120)
        self.music.place(x=260, y=630)
        self.music = Label(self.appGui, text=self.musicName)
        self.music.place(x=260, y=630)
        player.load("./music/%s"%str(self.musicName))
        self.length = self.GetMusicLength("./music/%s"%str(self.musicName[0:100]))
        player.play()
        fill = self.canvas.create_rectangle(1.5, 1.5, 0, 23, width=0, fill="green")
        while((pygame.mixer.music.get_pos()/1000) < self.length):
            count = int(pygame.mixer.music.get_pos()/1000/self.length*600)
            self.canvas.coords(fill, (0, 0, count, 100))
            self.appGui.update()
            time.sleep(0.02)

    def selectPlay(self,*kw):
        self.index = int(self.size - 1 - self.musicTree.curselection()[0])
        self.position = 0
        self.playMuisc()

if __name__ == "__main__":
    music = Music()
    music.getStarted()
