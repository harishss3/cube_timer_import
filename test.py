import json
from datetime import datetime

#################################################################################
option = -1
fh = None
category = None
cats = ["2x2x2","3x3x3","4x4x4","5x5x5","Megaminx","Others"]

def show_cats(cats):
    i=1
    for cat in cats:
        print(i,". ",cat,sep='')
        i = i +1

def make(t):
    mins = int(t)//60
    #Have to add code for greater than 10 minutes and for whole number time;
    sec = str(t - mins*60)
    mins = "0" + str(mins)
    while len(sec)!=6:
        if len(sec)>6:
            sec = sec[0:5]
            break 
        sec = sec + "0"
    tim = mins + ":" + sec
    return tim

def makeTime(record):
    times = record[1].split(":")
    mstime = int((round((float(times[1])),3) + 60*int(times[0]))*1000)
    time = [0, mstime]
    if record[4]=="yes":time[0]=2000
    if record[5]=="yes":time[0]=-1
    return time

##################################################################################

while True:
    print("Welcome! Please select desired option:\n\t1. Import from csTimer to Cube Timer\n\t2. Import from Cube Timer to csTimer")
    option = int(input())
    if option==1 or option ==2: break
    print("Please enter either 1 or 2 !")

if option == 1:
    print("Please choose the category: ")
    show_cats(cats)
    cat = int(input())
    #Add exception handling and others;
    category = cats[cat-1]

while True:
    f_name = input("Please enter the name of the file to be imported: ")
    try:
        fh = open(f_name)
        break
    except:
        print("File doesn't exist!")
fho = open("output.txt",'w')

#################################################################################
if option == 1:
    print("\"Category\";\"Time (MM:SS.SSS)\";\"Scrambler\";\"Date\";\"Penalty +2 (yes or no)\";\"DNF (yes or no)\";\"Section\"",file=fho)
    date = datetime.now().strftime("%Y-%m-%d %H:%M") #Have to add option to change date
    
    raw = fh.read()
    js = json.loads(raw)
    solves = js["session1"]
    
    for solve in solves:
        time = (solve[0][1])/1000
        time = make(time)
        penalty = "no"
        dnf = "no"
        if solve[0][0] == 2000:
            penalty = "yes"
        if solve[0][0] == -1:
            dnf = "yes"
        print(category,time,solve[1],date,penalty,dnf,";",file=fho,sep=';')

elif option == 2:
    data =  dict()
    data["Session1"] = [] #Add support for multi session
    for line in fh:
        if line.startswith("\""): continue
        record = line.split(";")
        time = makeTime(record)
        scramble = record[2]
        data["Session1"].append([time,scramble,"",""])
    print(data,file=fho)