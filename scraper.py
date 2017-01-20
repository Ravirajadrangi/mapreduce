import requests
from random import random
from time import sleep, time

fname = "data.csv"
fails = []
numfails = 0

# Read file
with open(fname, 'r') as fh:
    lines = fh.readlines()
    print("data read...")

# Process header
lines[0] = lines[0].strip() + ",Lat,Lng"+'\n'
with open("output.csv", 'w') as fh:
    fh.write(lines[0])
    print("header processed...")

lines = list(set(lines[1:]))

# Process data
def process(i):
    global numfails
    global fails
    try:
        x = lines[i].split(",")
        s = str(x[3]).strip()
        a = str(x[2]).strip()
    
        stub = 'http://maps.google.com/maps/api/geocode/json?address='
        query = stub + "+".join(a.split(' ')) + "+" + s
    
        r = requests.get(query).json()

        if r["status"] == "OK":
            
            lng = r["results"][0]['geometry']['location']['lng']
            lat = r["results"][0]['geometry']['location']['lat']
            lines[i] = lines[i].strip() + ",{},{}\n".format(lat,lng)
            
        else:
            # these probably failed because exceeded max requests per second
            print("sleeping... fails:{} index:{}".format(numfails, i))
            sleep(1)
            fails.append(i)
            numfails = numfails + 1
    
    except Exception as e:
        print(e)
        sleep(1)
        fails.append(i)

# First round
for i in range(1,len(lines)):
        process(i)

print("first round complete...")

# Retry failed requests
depth = 10
while depth > 0:
    for i in range(0, len(fails)):
        f = fails.pop(0)
        process(f)
    depth = depth - 1

# Retry stragglers
for y in range(0,len(fails)):
    sleep(abs(random()-.5))
    f = fails.pop(0)
    process(f)
    
# Save results to csv
print("scraper finished...")
with open("output.csv", 'a') as fh:
    fh.writelines(lines)

print("cannot find coordinates for these addresses:\n{}".format(fails))
with open("fails.csv", 'w') as fh:
    fh.writelines(fails)

print("complete!")

