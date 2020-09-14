import numpy as np
import datetime
print(datetime.date.today().day)


file_toPredict=[]
def load_file_toPredict():
    with open(r'C:\Users\fahmed\Desktop\ML for Logs\sample dataset\edf\test set\Success\EDFDump.log.2018-11-26.log') as f:
        file_toPredict.append(f.read())
        df2 = np.array(file_toPredict)
        df2.reshape(1, -1)
    return df2

df = load_file_toPredict()
df[0].replace("\n",'\n')
sections = df[0].split("Encompass ")

for i in range(0,len(sections)):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print("Section: ", i)
    #print(sections[i])
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


#Section 0 contains program arguments and other semantics not crucial to
# the outcome of the process

#Section 1 is the first run of prices

#Section 2 contains program arguments and other semantics not crucial to
# the outcome of the process

#Section 3 is 5 day shaped postions run
# check date to validate what the output here should be
# if time now is within 5 days of last of the month or beginning  then there will be an extra section that is the end of 5 day shaped
# so each number following this needs to be incremented by one
# or have 2 different code paths one for length 9 aka missing this part
# or length 10 aka it has this part

# Section 4 is Shaped Positions

# Section 5 End of Shaped Positions, but not much important here so we can ignore this

# Section 6 has second run of Prices

# Section 7 end of prices, but not much important here so we can ignore this

# section 8 is m2m

#section 9 is m2m end


