import csv
# Lists for all types of searches
crs=['1/10','1/8','1/6','1/4','1/3' ,'1/2', '1', '2', '3', '4', '5', '6', '7', '8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29']
environs=['Any', 'Underground', 'Deserts', 'Marshes', 'Forests', 'Hills', 'Mountains', 'Limbo', 'Aquatic', 'Plane', 'Plains']
types=[ 'Any', 'Aberration', 'Animal', 'Construct', 'Dragon', 'Elemental', 'Fey', 'Giant', 'Humanoid', 'Magical Beast', 'Monstrous Humanoid', 'Ooze', 'Outsider', 'Plant', 'Undead', 'Vermin']
creature_sizes    =   [ 'Any', 'Colossal', 'Diminutive', 'Gargantuan', 'Huge', 'Large', 'Medium', 'Small', 'Tiny']
alignments_list        =   [ 'Any' ]
lawfulnesses_list      =   [ 'Any' ]
# Two
numberlist = [['0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']]

# Three
numberlist.append(['0.333','0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17'])

# Four
numberlist.append(['0.25','0.5','0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'])

# 5-6
numberlist.append(['1.0/6.0','1.0/3.0','0.5','0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'])
numberlist.append(['1.0/6.0','1.0/3.0','0.5','0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'])

# 7-9
numberlist.append(['0.125','0.25','1.0/3.0','0.5','0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13','14'])
numberlist.append(['0.125','0.25','1.0/3.0','0.5','0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13','14'])
numberlist.append(['0.125','0.25','1.0/3.0','0.5','0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13','14'])

# 10-12
numberlist.append(['0.125','1.0/6.0','0.35','1.0/3.0','0.5','0.5','0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13'])
numberlist.append(['0.125','1.0/6.0','0.35','1.0/3.0','0.5','0.5','0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13'])
numberlist.append(['0.125','1.0/6.0','0.35','1.0/3.0','0.5','0.5','0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13'])

#pairslist1=['0.5','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']
#pairslist2=['1.0/3.0','0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','0.5','1','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']
z=range(1,21)
z=z+z
treasure=['300',' 600',' 900',' 1200',' 1600',' 2000',' 2600',' 3400',' 4500',' 5800',' 7500',' 9800',' 13000',' 17000',' 22000',' 28000',' 36000',' 47000',' 61000',' 80000',' 87000',' 96000',' 106000',' 116000',' 128000',' 141000',' 155000',' 170000',' 187000',' 206000',' 227000',' 249000',' 274000',' 302000',' 332000',' 365000',' 401000',' 442000',' 486000',' 534000']



#This section opens the csv of xpvalues and creates a list accessed as xplists[level of char][cr of monster]
f=open('src/xptable.csv','rb')
reader=csv.reader(f,delimiter=',',quotechar='"')
xplists=[]
for row in reader:
    xplists.append(row)
