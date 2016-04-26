import urllib2
import lxml.html
import csv

#Reads srdmonsters.xml and creates a dictionary in monsters.py
#Should exand to produce the lists in list.py
import xml.etree.ElementTree as ET


#function to write out each monster
#check for entries with multiple types is broken
def monster_dict_write(monster,output2):
	Environments=['Underground', 'plane',  'Any', 'Deserts', 'Marshes', 'Forests', 'Hills', 'Mountains', 'Limbo', 'Aquatic', 'Plane', 'Plains']
	Elements=['Air','Fire','Earth','Shadow', 'Water']
	multiflag=0
	name=monster.find('name').text
	name=name.replace(',','')
	cr=monster.find('challenge_rating').text
	size=monster.find('size').text
	type=monster.find('type').text
	init=monster.find('initiative').text
	hitdie=monster.find('hit_dice').text
	hitdie2=[]
	if 'plus' in hitdie:
		i=hitdie.index('p')
		j=hitdie.index('s')
		hitdie2=hitdie[j+1:]
		print hitdie2
		hitdie=hitdie[:i]
	if '(' in hitdie:
		i=hitdie.index('(')
		hitdie=hitdie[:i]
	i=hitdie.index('d')
	if '+' in hitdie:
		j=hitdie.index('+')
		hitdie=[hitdie[:i],hitdie[i+1:j],hitdie[j+1:]]
	else:
		hitdie=[hitdie[:i],hitdie[i+1:],'0']
	if len(hitdie2) > 1:
		if '(' in hitdie2:
			i=hitdie2.index('(')
			hitdie2=hitdie2[:i]
		i=hitdie2.index('d')
		if '+' in hitdie2:
			j=hitdie2.index('+')
			hitdie.append(hitdie2[:i])
			hitdie.append(hitdie2[i+1:j])
			hitdie.append(hitdie2[j+1:])
		else:
			hitdie.append(hitdie2[:i])
			hitdie.append(hitdie2[i+1:])
			hitdie.append('0')
	enviro=monster.find('environment').text
	envirotypes=enviro.split(' ')
	if envirotypes[-1] in Environments:
		if envirotypes[-1]=='plane':
			enviro='Aligned Plane'
		else:
			enviro=envirotypes[-1]

	elif envirotypes[-1] in Elements:
		enviro='Elemental Plane'
	for i in range(0,len(cr)):
		if cr[i]=='(':
			cr=cr[:i-1]
			break
			print "multiple types exist for monster"
			#print name, cr
			#print "enter name,cr of types manually"
	if len(hitdie)==3:
		if hitdie[0]=="1/2":
			hitdie[0]="0.5"
		output2.write("\n\t'"+name+"': ['"+str(cr)+"','"+size+"','"+type+"','"+enviro+"',["+hitdie[0]+","+hitdie[1]+","+hitdie[2]+"],'"+init+"'],")
	if len(hitdie)==6:
		if hitdie[0]=="1/2":
			hitdie[0]="0.5"
		if hitdie[3]=="1/2":
			hitdie[3]="0.5"
		output2.write("\n\t'"+name+"': ['"+str(cr)+"','"+size+"','"+type+"','"+enviro+"',["+hitdie[0]+","+hitdie[1]+","+hitdie[2]+","+hitdie[3]+","+hitdie[4]+","+hitdie[5]+"],'"+init+"'],")

	#output.write("\n\t'"+name+"': ["+str(cr)+",'"+size+"','"+type+"','"+enviro+"',[")
	#output.write(hitdie[0]+","+hitdie[1]+","+hitdie[2])
	#output.write("],'"+init+"'],")
	#output2.write("\n"+name+","+type+","+enviro+","+str(cr))
	return cr,size,type,enviro

def monster_full_write(monster):
	print monster.find('name').text
	outfile=monster.find('name').text
	out=open(outfile,'wb')
	out.write('Size:\t'+monster.find('size').text+'\n')
	out.write('HD:\t'+monster.find('hit_dice').text+'\n')
	out.write('Initiative:\t'+monster.find('initiative').text+'\n')
	out.write('speed:\t'+monster.find('speed').text+'\n')
	out.write('AC\t'+monster.find('armor_class').text+'\n')
	out.write('Base Attack\t'+monster.find('base_attack').text+'\n')
	out.write('Attack:\t'+monster.find('attack').text+'\n')
	out.write('Full Attack:\t'+monster.find('full_attack').text+'\n')
	out.write('Grapple:\t'+monster.find('grapple').text+'\n')
	out.write('Space:\t'+monster.find('space').text+'\n')
	out.write('Reach:\t'+monster.find('reach').text+'\n')
	out.write('Saves:\t'+monster.find('saves').text+'\n')
	out.write('Abilities:\t'+monster.find('abilities').text+'\n')
	out.write('Skills:\t'+monster.find('skills').text+'\n')
	out.write('Feats:\t'+monster.find('feats').text+'\n')


tree = ET.parse('srdmonsters.xml')
#out=open('monstersdictionary.py','wb')
monsters=tree.findall('monster')
out2=open('../monstersdictionary.py','wb')
out2.write("monst_dict={\n")
#out.write("# List of Monsters\n# 'Monster Name': [Monster Manual Page, 'Challenge Rating number', Experience Points, Size, Type]")
#out.write("\n# 'Key'         :      					 [0],                  [1],					[2]  		  [3]  [4]')")
#out.write("\nmonst_dict={")

crlist=[];envirlist=[];sizelist=[];typelist=[]
crmax=0
for monster in monsters:
	#cr,size,type,enviro=monster_dict_write(monster,out,out2)
	cr,size,type,enviro=monster_dict_write(monster,out2)

	if cr > crmax:
		crmax=cr
	if enviro not in envirlist:
		envirlist.append(enviro)
	if type not in typelist:
		typelist.append(type)
	if size not in sizelist:
		sizelist.append(size)
	#monster_full_write(monster)
out2.write("}")
crlist=[0.25,0.5]+range(1,int(crmax),1)
envirlist.sort()
envirlist=['Any']+envirlist
sizelist.sort()
sizelist=['Any']+sizelist
typelist.sort()
typelist=['Any']+typelist
#finish monster file
#out.write("}")
#out.close()
