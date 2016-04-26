#this is the class for a combatant.
#it contains the row frame and widgets.
#also all details about combatant
import random
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import os
import csv

from globals import Monster
import rows
from player import player

class fight:
    def __init__(self,builder,globaldata):
        #load objects
        fightbox=builder.get_object("fightframe")
        reloadbutton=builder.get_object("reloadbutton")
        self.fightbutton=builder.get_object("fightbutton")
        self.nextbutton=builder.get_object("nextbutton")
        self.partychooser=builder.get_object("partychooser")
        self.enemychooser=builder.get_object("enemychooser")
        self.partyrowbox=builder.get_object("partyrowbox")
        self.enemyrowbox=builder.get_object("enemyrowbox")

        #connect signals
        reloadbutton.connect("clicked",self.on_reloadbutton_clicked)
        self.fightbutton.connect("clicked",self.on_fightbutton_clicked)
        self.nextbutton.connect("clicked",self.on_nextbutton_clicked)
        #basic set up
        self.globaldata=globaldata
        self.enemychooser_fill(self.enemychooser)
        self.enemychooser.set_active(0)
        self.partychooser_fill(self.partychooser)
        self.partychooser.set_active(0)
        #initial set up of rows
        self.baddies=globaldata.selected
        self.globaldata=globaldata

        self.goodies=[]
        for player in globaldata.players:
            goodies.append(playerrow(fightbox,player))
        self.baddies=[]
        for monst in globaldata.selected:
            baddies.append(enemyrow(fightbox,monst))

####################################################
#Button fuctions                                   #
####################################################

    def on_reloadbutton_clicked(self,button):

        self.players=[]
        name=self.partychooser.get_active_text()
        if len(name)>0:
            name=name+".par"
            j=0
            with open("userdata/"+name, 'rb') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in reader:
                    self.players.append(player(row))
                    j+=1
            self.globaldata.players=self.players
        name=self.enemychooser.get_active_text()
        if (len(name)>0):
            name=name+".enc"
            j=0
            with open("userdata/"+name, 'rb') as csvfile:
                self.globaldata.selected=[]
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                for row in reader:
                    monst=Monster(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                    self.globaldata.selected.append(monst)

        self.create_rows()

    def on_fightbutton_clicked(self,button):
        for goody in self.goodies:
            if goody.initiative==0:
                goody.on_initrollbutt_clicked(goody.initrollbutton)
        for baddy in self.baddies:
            if baddy.initiative==0:
                baddy.on_initrollbutt_clicked(baddy.initrollbutton)
        self.initsort()
        self.currentplayer=0
        self.zippedinits[self.currentplayer][1].rowframe.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("purple"))

    def on_nextbutton_clicked(self,button):
        self.zippedinits[self.currentplayer][1].rowframe.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("grey"))
        self.currentplayer+=1
        if self.currentplayer==len(self.zippedinits):
            self.currentplayer=0
        self.zippedinits[self.currentplayer][1].rowframe.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("purple"))




####################################################
#Fight Functions                                   #
####################################################
    def initsort(self):
        #first sort goodies
        #create list of initiatives
        initiatives=[]
        for goody in self.goodies:
            print initiatives
            initiatives.append(goody.initiative)
        #zip together and sort
        self.zippedinits=zip(initiatives,self.goodies)
        self.zippedinits.sort()
         #now reorder each  goody by it's position in sorted list
        for goody in self.goodies:
            pos=self.zippedinits.index((goody.initiative,goody))
            print pos,'ho'
            self.partyrowbox.reorder_child(goody.rowframe,pos)

        #repeat for baddies
        initiatives=[]
        for baddy in self.baddies:
            initiatives.append(baddy.initiative)
        zipinits=zip(initiatives,self.baddies)
        zipinits.sort()
        for baddy in self.baddies:
            pos=zipinits.index((baddy.initiative,baddy))
            print pos
            self.enemyrowbox.reorder_child(baddy.rowframe,pos)

        self.zippedinits+=zipinits
        self.zippedinits.sort()


####################################################
#Set up of page                                    #
####################################################

    #function to produce all rows of combatants
    def create_rows(self):
        for goody in self.goodies:
            self.partyrowbox.remove(goody.rowframe)
        self.goodies=[]
        for player in self.globaldata.players:
            self.goodies.append(rows.playerrow(self.partyrowbox,player))

        for baddy in self.baddies:
            self.enemyrowbox.remove(baddy.rowframe)
        self.baddies=[]
        namelist=[]
        for enemy in self.globaldata.selected:
            namecount=namelist.count(enemy.name)
            namelist.append(enemy.name)
            if namecount >0:
                enemy.name=enemy.name+" "+str(namecount+1)
            self.baddies.append(rows.enemyrow(self.enemyrowbox,enemy))

    def partychooser_fill(self,box):
        files=os.listdir('./userdata')
        for file in files:
            if file[-4:]=='.par':
                box.append_text(file[:-4])

    def enemychooser_fill(self,box):
        files=os.listdir('./userdata')
        for file in files:
            if file[-4:]=='.enc':
                box.append_text(file[:-4])