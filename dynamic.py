import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import globals
import combatant
import monster
import party


globaldata=globals.globaldat()
builder = Gtk.Builder()
builder.add_from_file("mainwindow.glade")

win = builder.get_object("mainwindow")

win.set_default_size(800,600)
win.connect("delete-event", Gtk.main_quit)
#win.add(box)

#set up frames by loading them from .glade file
encounterframe=builder.get_object("encounterdummy")
playerframe=builder.get_object("partyframe")

#send named frames from tabbed window to classes that deal with them
encounter=monster.encounter(builder,globaldata)
players=party.party(builder,globaldata)
combat=combatant.fight(builder,globaldata)
win.show_all()

Gtk.main()

