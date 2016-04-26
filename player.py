import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
class player:
    def __init__(self,stats):
        builder=Gtk.Builder()
        builder.add_from_file("playerrow.glade")
        self.playerrow=builder.get_object("playerrow")
        self.hpbox=builder.get_object("hpbox")
        self.namebox=builder.get_object("namebox")
        self.eclbox=builder.get_object("eclbox")
        
        self.name=stats[0]
        self.ecl=stats[1]
        self.hptot=stats[2]
    def insert_stats(self,box):
        box.pack_start(self.playerrow,expand=False, fill=True, padding=0)

        self.namebox.set_text(self.name)
        self.hpbox.set_text(self.hptot)
        self.eclbox.set_text(self.ecl)

    def getinfo(self):
        self.name=self.namebox.get_text()
        self.ecl=self.eclbox.get_text()
        self.hptot=self.hpbox.get_text()
        return [self.name,str(self.ecl),(self.hptot)]


