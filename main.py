import json
import sys

def stringMetric(s, t):
    output = []
    for i in range(0, len(t)):
        metric = 0
        for j in range(0, min(len(s.split()[0]), len(t[i]))):
            if s.split()[0][j].lower() == t[i][j].lower():
                metric += 1
        output.append(metric)
    index = [i for i, j in enumerate(output) if j == max(output)]
    if len(index) == 1:
        return t[index[0]]
    else:
        return stringMetric(s.split()[1], t)

# Opening contributors.json, and putting all contributors into a list
with open('contributors.json') as f:
    contributor = json.load(f)

contributors = []

contributor_max = 0
for i in range(0, len(contributor)):
    contributors.append(contributor[i]['login'])
    if len(contributor[i]['login']) > contributor_max:
        contributor_max = len(contributor[i]['login'])

if contributor_max % 2 != 0:
    contributor_max += 1

user = " "*((contributor_max - 4) / 2) + "User" + " "*((contributor_max - 4) / 2)
Date_Time = " "*6 + "Date/Time" + " "*6

with open('commits.json') as f:
    data = json.load(f)

output = open("log.txt", "w+")

dash = "-"*int(sys.argv[1])

message = " "*((int(sys.argv[1]) - (contributor_max + 48)) / 2 - 1) + "Message" + " "*((int(sys.argv[1]) - (contributor_max + 48)) / 2 - 1)

ctype = " "*5 + "Type" + " "*5

output.write("%s\n" % dash)

output.write("| %s |%s|%s|%s\n" % (user, Date_Time, ctype, message))

output.write("%s\n" % dash)

for i in range(0, len(data)):
    if data[i]['author'] is not None:
        output.write("| %s " % data[i]['author']['login'] + " "*(contributor_max - len(data[i]['author']['login'])))
    
    elif data[i]['commit']['author']['name'] in contributors:
        output.write("| %s " % data[i]['commit']['author']['name'] + " "*(contributor_max - len(data[i]['commit']['author']['name'])))

    else:
        output.write("| %s " % stringMetric(data[i]['commit']['author']['name'], contributors) + " "*(contributor_max - len(stringMetric(data[i]['commit']['author']['name'], contributors))))
    
    output.write("| %s" % data[i]['commit']['author']['date'][:10] + " " + data[i]['commit']['author']['date'][11:len(data[i]['commit']['author']['date']) - 1])
    
    output.write(" | %s " % "Commit" + " "*5)
    
    temp = data[i]['commit']['message'].replace("\n", " ")

    length = int(sys.argv[1]) - (contributor_max + 44)
    
    output.write(" | %s |\n" % (temp[:length] + " "*(length - len(temp[:length]))))

    while len(temp[:length]) >= length:
        temp = temp[length:]
        output.write("| %s |\n" %(" "*(contributor_max + 1) + "|" + " "*21 + "|" + " "*14 + "| " + temp[:length] + " "*(length - len(temp[:length]))))
        temp = temp[length:]

    output.write("%s\n" % dash)

with open('issues.json') as f:
    issue = json.load(f)
    
for i in range(0, len(issue)):
    output.write("| %s " % issue[i]["user"]["login"] + " "*(contributor_max - len(issue[i]["user"]["login"])))
    output.write("| %s" % issue[i]["created_at"][:10] + " " + issue[i]["created_at"][11:len(issue[i]["created_at"]) - 1])
    output.write(" | %s " % "Issue" + " "*6)
    output.write(" | %s \n" % issue[i]["title"])
    output.write("%s\n" % dash) 
