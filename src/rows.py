import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gdk
import random
class playerrow:
	#on intialisation, load the frame
    def __init__(self,box,player):
        self.player=player
        gladefile="combatantrow.glade"
        builder=Gtk.Builder()
        builder.add_from_file(gladefile)

        #get all the widgets that are necessary.
        #buttons
        self.healbutton=builder.get_object("healbutt")
        self.initrollbutton=builder.get_object("initrollbutt")
        self.rowframe=builder.get_object("combatantframe")
        #labels
        self.hplabel=builder.get_object("hplabel")
        self.namelabel=builder.get_object("namelabel")
        #imputs
        self.initbox = builder.get_object("initbox")
        self.damageentry=builder.get_object("damageentry")
        #change monster hit die roll to a refresh
        self.hpbutton=builder.get_object("hitrollbutt")
        self.hpbutton.set_label('Refresh')

        #connect signals
        builder.connect_signals(self) 
        box.pack_start(self.rowframe,True,True,0)

        #general set up
        self.namelabel.set_text(self.player.name)
        self.hplabel.set_text(self.player.hptot)
        self.hpcurrent=int(self.player.hptot)

        self.initiative=0
    #FUNCTIONS FOR WHEN BUTTONS ARE PRESSED
    def on_initrollbutt_clicked(self,button):
        self.initiative = random.randint(1,20)
        self.initbox.set_text(str(self.initiative))

    def on_initsetbutt_clicked(self,button):
        self.initiative=int(self.initbox.get_text())
        self.initbox.set_text(str(self.initiative))

    def on_hitrollbutt_clicked(self,button):
        self.hpcurrent=self.player.hptot
        self.update_hplabel()

    def on_dambutt_clicked(self,button):
        damage=int(self.damageentry.get_text())
        self.hpcurrent-=damage
        self.update_hplabel()
        if (self.hpcurrent<1):
            self.rowframe.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("orange"))
        if (self.hpcurrent<0):
            self.rowframe.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("red"))

    def on_healbutt_clicked(self,button):
        heald=int(self.damageentry.get_text())
        self.hpcurrent+=heal
        if self.hpcurrent>int(self.player.hptot):
            self.hpcurrent=int(self.player.hptot)
        self.update_hplabel()
    #######################################
    #MORE GENERIC FUNCTIONS               #
    #######################################
    def update_hplabel(self):
        self.hplabel.set_text(str(self.hpcurrent)+'/'+self.player.hptot)


class enemyrow:
    #on intialisation, load the frame
    def __init__(self,box,enemy):
        self.enemy=enemy
        gladefile="combatantrow.glade"
        builder=Gtk.Builder()
        builder.add_from_file(gladefile)

        #get all the widgets that are necessary.
        #buttons
        self.healbutton=builder.get_object("healbutt")
        self.initrollbutton=builder.get_object("initrollbutt")
        self.rowframe=builder.get_object("combatantframe")
        #labels
        self.hplabel=builder.get_object("hplabel")
        self.namelabel=builder.get_object("namelabel")
        #imputs
        self.initbox = builder.get_object("initbox")
        self.damageentry=builder.get_object("damageentry")


        #connect signals
        builder.connect_signals(self) 
        box.pack_start(self.rowframe,True,True,0)

        #general set up
        self.namelabel.set_text(self.enemy.name)
        self.initiative=0

    def on_initrollbutt_clicked(self,button):
        self.initiative = random.randint(1,20)
        self.initbox.set_text(str(self.initiative))

    def on_initsetbutt_clicked(self,button):
        self.initiative=int(self.initbox.get_text())

    #Roll monster's hitdie. For some reason, monsters have hitdie lists when created
    #but when retrieved for this funciton, come as strings
    def on_hitrollbutt_clicked(self,button):
        hitdie=self.enemy.hitdie[1:-1].split(',')
        self.hptot=0
        for i in range(0,int(hitdie[0])):
            self.hptot+=random.randint(1,int(hitdie[1]))
            print self.hptot
        self.hptot+=int(hitdie[2])
        self.hplabel.set_text(str(self.hptot)+"/"+str(self.hptot))

    def on_dambutt_clicked(self,button):
        damage=int(self.damageentry.get_text())
        self.hpcurrent-=damage
        self.update_hplabel()
        if (self.hpcurrent<1):
            self.rowframe.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("orange"))
        if (self.hpcurrent<0):
            self.rowframe.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("red"))

    def on_healbutt_clicked(self,button):
        heald=int(self.damageentry.get_text())
        self.hpcurrent+=heal
        if self.hpcurrent>self.hptot:
            self.hpcurrent=self.hptot
        self.update_hplabel()