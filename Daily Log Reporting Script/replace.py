
def func():
    f = open(r"C:\Users\fahmed\Downloads\LPG_Map_Vantage-03.24.2020_Final.csv","r")
    for x in f:
        if(len(x) > 5):
            x = x.replace("_PEAK","")
            x = x.replace("_7x8","")
            x = x.replace("_2x16","")
            x = x.replace("_1x16","")
            s=''
            s += '(\'' + x.replace(""",""","""\',\'""")+ '\'' + '),'
            
            print(s)
    
    #string = string.replace(""",""","""\',\'""")+ '\''
    #string2 = string.replace("PEAK", "7x8") 
    #string3 = string.replace("PEAK", "2x16")
    #print(string)
    #print(string2)
    #print(string3)

func()
