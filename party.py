import gi
import csv
import os
from player import player
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
class party:
	#on intialisation, load the frame
    def __init__(self,builder,globaldata):
        #get objects relevent to party tab
        thisframe=builder.get_object("partyframe")
        addbutton=builder.get_object("addbutton")
        savebutton=builder.get_object("savebutton")
        self.playersbox=builder.get_object("playersbox")
        self.partynamebox=builder.get_object("partynamebox")
        self.partybox_fill(self.partynamebox)
        #connect signals
        addbutton.connect("clicked",self.on_addbutton_clicked) 
        savebutton.connect("clicked",self.on_savebutton_clicked)
        self.partynamebox.connect("changed",self.on_partynamebox_changed)
        self.players=[]
        self.globaldata=globaldata

    def on_addbutton_clicked(self,button):
        print "hi"
        self.players.append(player(["","",""]))
        self.players[-1].insert_stats(self.playersbox)

    def on_savebutton_clicked(self,button):
        name=self.partynamebox.get_active_text()
        name=name+".par"
        file=open("userdata/"+name,"wb")
        writer = csv.writer(file,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        for player in self.players:
            line=player.getinfo()
            if line[0]!="":
                writer.writerow(line)
        self.globaldata.players=self.players

    def partybox_fill(self,box):
        files=os.listdir('./userdata')
        self.parties=[]
        for file in files:
            if file[-4:]=='.par':
                self.parties.append(file[:-4])
                box.append_text(file[:-4])

    def on_partynamebox_changed(self,box):
        for char in self.players:
            self.playersbox.remove(char.playerrow)
        self.players=[]
        name=self.partynamebox.get_active_text()
        name=name+".par"
        j=0
        with open("userdata/"+name, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                self.players.append(player(row))
                self.players[j].insert_stats(self.playersbox)
                j+=1
        self.globaldata.players=self.players