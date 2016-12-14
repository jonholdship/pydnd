import gi
from src import lists
import os
import csv
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
from globals import Monster

#Class to handle encounter window ingeneral
class encounter:
    def __init__(self,builder,globaldata):
        #deal with buttons
        self.globaldata=globaldata
        monstaddbutton=builder.get_object("monstadd")
        monstdelbutton=builder.get_object("monstdel")
        encsavebutton=builder.get_object("encsavebutton")
        encloadbutton=builder.get_object("encloadbutton")
        monstdelbutton.connect("clicked",self.monstdel_pressed)
        monstaddbutton.connect("clicked",self.monstadd_pressed)
        encsavebutton.connect("clicked",self.save_encounter)
        encloadbutton.connect("clicked",self.load_encounter)
        #deal with filtering boxes
        self.environbox=builder.get_object("environbox")
        self.maxcrbox=builder.get_object("maxcrbox")
        self.mincrbox=builder.get_object("mincrbox")
        self.typebox=builder.get_object("typebox")
        self.sizebox=builder.get_object("sizebox")
        self.searchbar=builder.get_object("monstersearch")
        selectwindow=builder.get_object("selectwindow")   
        filterwindow=builder.get_object("filterwindow")

        #deal with labels
        self.crlabel=builder.get_object("crlabel")
        self.xplabel=builder.get_object("xplabel")
        self.treasurelabel=builder.get_object("treasurelabel")

        self.encounterbox=builder.get_object("encounterbox")
        
        maingrid=builder.get_object("encountermaingrid")
        filterlist=builder.get_object("filterlist")

        lists.environs.sort()
        
        #set filter boxes up
        for environ in lists.environs:
            self.environbox.append_text(environ)
        self.environbox.set_active(0)

        for cr in lists.crs:
            self.maxcrbox.append_text(cr)
            self.mincrbox.append_text(cr)
        self.mincrbox.set_active(0)
        self.maxcrbox.set_active(20)
        for type in lists.types:
            self.typebox.append_text(type)
        self.typebox.set_active(0)

        for size in lists.creature_sizes:
            self.sizebox.append_text(size)
        self.sizebox.set_active(0)

        self.maxcrbox.connect("changed",self.filterbox_changed_cb)
        self.mincrbox.connect("changed",self.filterbox_changed_cb)
        self.typebox.connect("changed",self.filterbox_changed_cb)
        self.environbox.connect("changed",self.filterbox_changed_cb)
        self.sizebox.connect("changed",self.filterbox_changed_cb)
        self.searchbar.connect("search-changed",self.filterbox_changed_cb)
        #set up scroll windows of monsters lists
        self.filterlist=monstlist(filterwindow)
        self.selectlist=monstlist(selectwindow)
        #self.filterlist.fill(globaldata)

        self.encounterbox_fill(self.encounterbox)

########################################################
# Buttons and Inputs                                   #
########################################################
    def filterbox_changed_cb(self,crbox):
        chosencr=self.maxcrbox.get_active_text()
        maxcrindex=lists.crs.index(chosencr)
        chosencr=self.mincrbox.get_active_text()
        mincrindex=lists.crs.index(chosencr)


        self.filterlist.cr_filter(mincrindex,maxcrindex,lists.crs,self.globaldata)
        print "cr"
        #filter by type
        chosentype=self.typebox.get_active_text()
        self.filterlist.type_filter(chosentype,self.globaldata)
        
        print "type"
        #filter by environment
        chosenenvir=self.environbox.get_active_text()
        self.filterlist.envir_filter(chosenenvir,self.globaldata)

        #filter by size
        chosensize=self.sizebox.get_active_text()
        self.filterlist.size_filter(chosensize,self.globaldata)

        print "size"
        #filter by text
        searchtext=self.searchbar.get_text()
        self.filterlist.text_filter(searchtext)
        print "search"

        #redraw list
        self.filterlist.redraw_list();
        print "draw"

    def monstdel_pressed(self,button):
        self.selectlist.remove_monster()
        self.globaldata.selected=self.selectlist.monsters
        self.combine_crs()

    def monstadd_pressed(self,button):
        print self.globaldata.players
        selectedmonster=self.filterlist.get_selected_monster()
        self.selectlist.add_monster(selectedmonster)
        self.globaldata.selected=self.selectlist.monsters
        self.combine_crs()

########################################################
# Encounter load/save                                  #
########################################################
    def encounterbox_fill(self,box):
        files=os.listdir('./userdata')
        self.encs=[]
        for file in files:
            if file[-4:]=='.enc':
                self.encs.append(file[:-4])
                box.append_text(file[:-4])


    def save_encounter(self,button):
        name=self.encounterbox.get_active_text()
        name=name+".enc"
        file=open("userdata/"+name,"wb")
        writer = csv.writer(file,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
        for monster in self.selectlist.monsters:
            line=monster.getinfo()
            if line[0]!="":
                writer.writerow(line)
        self.globaldata.selected=self.selectlist.monsters
        self.encounterbox_fill(self.encounterbox)

    def load_encounter(self,button):
        name=self.encounterbox.get_active_text()
        name=name+".enc"
        j=0
        with open("userdata/"+name, 'rb') as csvfile:
            self.selectlist.monsters=[]
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                monst=Monster(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
                self.selectlist.add_monster(monst)
        self.globaldata.selected=self.selectlist.monsters
        self.selectlist.redraw_list()
        self.combine_crs()
           
########################################################
# Encounter stats                                      #
########################################################

    def combine_crs(self):
        crlist=[]
        monsters=self.globaldata.selected
        for monst in monsters:
            crlist.append(monst.challenge_rating)
                # loop over monster crs and join until there is only one
        matchflag=1
        newcrlist=[]
        while len(crlist)>1:
            #loop over monster crs and join any that are same value
            while matchflag>0:
                matches=0
                #go through lists of crs
                for i in lists.crs:
                    #count how many times that cr turns up in current monsters
                    number=crlist.count(i)
                    #12 is too many,  DM guide doesn't go that high, so add excess to new list
                    #and proceed with 12
                    if number >12:
                        for j in range(number-12):
                            newcrlist.append(i)
                        number=12
                    #if we counted multiple of the current cr in monsters, combine
                    if number>1:
                        j=lists.numberlist[number-2].index(i)
                        if newcrlist.count(j+1) >0:
                            matches+=1
                        newcrlist.append(str(j+1))
                    if number==1:
                        newcrlist.append(i)
                crlist=newcrlist
                print crlist
                newcrlist=[]
                if matches==0:
                    matchflag=0
                    
            #now only different crs remain, combine pairs using function from lists
            print crlist
            if len(crlist) > 1:
                crlist.sort()
                print crlist
                newcr=0.58*(float(crlist[0])+float(crlist[1]))
                newcr=int(newcr)
                if newcr>int(crlist[1]):
                    newcrlist=[str(newcr)]
                else:
                    newcrlist=[crlist[1]]
                if len(crlist)>2:
                    for i in range(2,len(crlist)):
                        newcrlist.append(crlist[i])
                #update cr list ready for next iteration, starting again from combining matches
                crlist=newcrlist
                newcrlist=[]
                print crlist

        #print cr to screen and call calculations for xp and treasure
        self.crtot=crlist[0]
        self.crlabel.set_text(str(self.crtot))
        self.get_encounter_treasure()
        self.get_encounter_xp()

    #calculate xp, currently for first player only
    def get_encounter_xp(self):
        crlist=[]
        #get all monster crs, xp done per monster rather than combined
        for monster in self.globaldata.selected:
            crlist.append(monster.challenge_rating)
        #this function should do xp per character. for now test with a single level 1 character
        level=self.globaldata.players[0].ecl
        partysize=len(self.globaldata.players)
        xptot=0
        #work out xp for all monsters and add to total. Then divide by number of players
        for cr in crlist:
            if cr >= 1:
                xptot+=int(lists.xplists[int(level)-1][int(cr)-1])
        xptot/=partysize
        self.xplabel.set_text(str(xptot))

    def get_encounter_treasure(self):
        i=int(self.crtot)
        i-=1
        treasure_value=lists.treasure[i]
        self.treasurelabel.set_text(treasure_value)

#class to handle to the fliter and selected lists
class monstlist:
    def __init__(self,window):
     # the data in the model (three strings for each row, one for each
            # column)

        columns = ["CR","Name"]
        self.monsters=[]
        self.listmodel = Gtk.ListStore(str, str)
        # append the values in the model
        for i in range(len(self.monsters)):
            self.listmodel.append(monsters[i])

        # a treeview to see the data stored in the model
        self.view = Gtk.TreeView(model=self.listmodel)
        # for each column
        for i in range(len(columns)):
            # cellrenderer to render the text
            cell = Gtk.CellRendererText()
            # the text in the first column should be in boldface
            if i == 0:
                cell.props.weight_set = True
            # the column is created
            col = Gtk.TreeViewColumn(columns[i], cell, text=i)
            col.set_sort_column_id(i)
            # and it is appended to the treeview
            self.view.append_column(col)

            window.add_with_viewport(self.view)
    
    def get_selected_monster(self):
        selected=self.view.get_selection()
        model,iter=selected.get_selected()
        name=model[iter][1]
        for monster in self.monsters:
            if monster.name == name:
                return monster

    def redraw_list(self):
        print "redraw start"
        #remove all the entries in the model

        if len(self.listmodel) != 0:
            for i in range(len(self.listmodel)):
                iter = self.listmodel.get_iter(0)
                self.listmodel.remove(iter)

        #self.listmodel.clear()
        print "clear"
        #add  monsters list to model again
        for i in range(len(self.monsters)):
            self.listmodel.append([self.monsters[i].challenge_rating,self.monsters[i].name])
    

    #this function is to initially fill filterlist
    def fill(self, globaldata):
        #empty list of monsters
        self.monsters=[]
        for key in globaldata.monsters_dict:
            #append monsters to list
            self.monsters.append(globaldata.monsters_dict[key])
            self.monsters.sort()  
        self.redraw_list() 

    def add_monster(self,monster):
        self.monsters.append(monster)
        self.redraw_list()

        

    #remove the selected monster from list
    def remove_monster(self):
        #use get seelected monster function to get current selection
        toremove=self.get_selected_monster()
        #python list.remove() only removes one copy from list so easy to use
        self.monsters.remove(toremove)
        #sort does not work
        self.monsters.sort()

        self.redraw_list()

    def cr_filter(self, minindex,maxindex,crlist,globaldata):
        self.monsters=[]
        for key in globaldata.monsters_dict:
            #append monsters to list
            monster=globaldata.monsters_dict[key]
            currentindex=crlist.index(monster.challenge_rating)
            if (currentindex >=minindex and currentindex <= maxindex):
                self.monsters.append(monster)

    def type_filter(self,typefilter,globaldata):
        old=self.monsters
        self.monsters=[]
        for monster in old:
            if (monster.type == typefilter) or (typefilter =="Any") or (monster.type=="Any"):
                self.monsters.append(monster)

    def envir_filter(self,envirfilter,globaldata):
        old=self.monsters
        self.monsters=[]
        for monster in old:
            if (monster.environment == envirfilter) or (envirfilter =="Any")or (monster.environment=="Any"):
                self.monsters.append(monster)

    def size_filter(self,sizefilter,globaldata):
        old=self.monsters
        self.monsters=[]
        for monster in old:
            if (monster.size == sizefilter) or (sizefilter =="Any")or (monster.size=="Any"):
                self.monsters.append(monster)

    def text_filter(self,textfilter):
        old=self.monsters
        self.monsters=[]
        for monster in old:
            if (textfilter.upper() in monster.name.upper()):
                self.monsters.append(monster)