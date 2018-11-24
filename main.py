import json
import sys
import numpy as np
import os
import datetime
from datetime import timedelta

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
        #return stringMetric(s.split()[1], t)
        return "*"

def cleanContributors(contributors):
    output = []
    for i in range(0, len(contributors)):
        output.append(contributors[i]['login'])
    return output
    

def cleanCommits(contributors, commits):
    output = np.zeros((len(commits), 4), dtype=object)
    
    for i in range(0, len(commits)):
        # Clean committers
        if commits[i]['author'] is not None:
            output[i][0] = commits[i]['author']['login']
        elif commits[i]['commit']['author']['name'] in contributors:
            output[i][0] = commits[i]['commit']['author']['name']
        else:
            output[i][0] = stringMetric(commits[i]['commit']['author']['name'], contributors)

        # Clean date/time
        output[i][1] = commits[i]['commit']['author']['date'][:10] + " " + commits[i]['commit']['author']['date'][11:len(commits[i]['commit']['author']['date']) - 1]

        # List of string "Commit"
        output[i][2] = "Commit"

        # Clean messages
        output[i][3] = commits[i]['commit']['message'].replace('\r', '').replace('\n', '').replace('\t', '')

    return output

def cleanIssues(issues):
    output = np.zeros((len(issues), 4), dtype=object)
    
    for i in range(0, len(issues)):
        # Clean committers
        output[i][0] = issues[i]["user"]["login"]

        # Clean date/time
        output[i][1] = issues[i]["created_at"][:10] + " " + issues[i]["created_at"][11:len(issues[i]["created_at"]) - 1]
        
        # List of string "Issue"
        output[i][2] = "Issue"

        # Clean messages
        output[i][3] = issues[i]["title"].replace('\n', '').replace('\r', '')
    
    return output

def cleanPulls(pulls):
    output = np.zeros((len(pulls), 4), dtype=object)
    
    for i in range(0, len(pulls)):
        output[i][0] = pulls[i]["user"]["login"]
        output[i][1] = pulls[i]["created_at"][:10] + " " + pulls[i]["created_at"][11:len(pulls[i]["created_at"]) - 1]
        output[i][2] = "Pull Request"
        output[i][3] = (pulls[i]["title"] + " " + pulls[i]["body"]).replace('\n', '').replace('\r', '')
    
    return output

def main():
    # Name of repo inputted by user
    repo = sys.argv[1]

    # Opens contributors.json, extracts contributor attributes, and puts info into 'contributors'
    with open(repo + '/contributors.json') as f:
        contributors = json.load(f)
    contributors = cleanContributors(contributors)

    # 'contributor_max'/dash/etc help with formatting table
    contributor_max = 0
    for i in range(0, len(contributors)):
        if len(contributors[i]) > contributor_max:
            contributor_max = len(contributors[i])

    # 'header' will be the header for all sprint cycles 
    dash = "-"*(int(sys.argv[2]) + 1)
    user = " "*((contributor_max - 4) // 2 + 1) + "User" + " "*((contributor_max - 4) // 2 + 1)
    if contributor_max % 2 == 0:
        user += " "
    date_time = " "*6 + "Date/Time" + " "*6
    ctype = " "*5 + "Type" + " "*5
    message = " "*((int(sys.argv[2]) - (contributor_max + 48)) // 2) + "Message" + " "*((int(sys.argv[2]) - (contributor_max + 48)) // 2) + "|"
    
    header = str.format("%s\n|%s|%s|%s|%s\n%s\n" % (dash, user, date_time, ctype, message, dash))

    output = open(repo + "/log.txt", "w+")

    #output.write("%s" % header)

    data = np.array([])

    for filename in os.listdir(repo + '/commits'):
        with open(repo + '/commits/' + filename) as f:
            commit = json.load(f)
            if data.size == 0:
                data = cleanCommits(contributors, commit)
            else:
                data = np.vstack((data, cleanCommits(contributors, commit)))
    
    with open(repo + '/issues.json') as f:
        issue = json.load(f)
        data = np.vstack((data, cleanIssues(issue)))

    with open(repo + '/pulls.json') as f:
        pull = json.load(f)
        data = np.vstack((data, cleanPulls(pull)))

    data_temp = data
  
    data = np.array([])

    for i in sorted(range(len(data_temp[:, 1])), key=lambda k: data_temp[:, 1][k], reverse=True):
        if data.size == 0:
            data = data_temp[i]
        else:
            data = np.vstack((data, data_temp[i]))

    orig = data[len(data) - 1][1]
    fin = data[0][1]
    
    choice = input("Earliest contribution is " + data[len(data) - 1][1] + " and latest contribution is " + data[0][1] + ". Would you like to change these dates in the report? (Enter y/n) ")
    
    while choice != 'y' and choice != 'n':
        choice = input("Incorrect input. Please enter (y) to change dates, or (n) to keep dates. ")

    if choice == 'y':
        orig = input("Please enter beginning date: (mm/dd/yyyy Format) ")
        orig = datetime.datetime(int(orig[6:10]), int(orig[0:2]), int(orig[3:5]))
        fin = input("Please enter end date: (mm/dd/yyyy Format) ")
        fin = datetime.datetime(int(fin[6:10]), int(fin[0:2]), int(fin[3:5]))
        sprint_cycle = input("Please enter sprint cycle length: (in days) ")
    
    else:
        orig = datetime.datetime(int(orig[0:4]), int(orig[5:7]), int(orig[9:11]))
        fin = datetime.datetime(int(fin[0:4]), int(fin[5:7]), int(fin[9:11]))
        sprint_cycle = 7

    #print(x + timedelta(days=int(sprint_cycle)))

    dash_report = "-"*(int(sys.argv[2]) - 86)

    sprints = np.array([])

    while orig <= fin:
        next_date = orig + timedelta(days=int(sprint_cycle - 1))
        if len(sprints) == 0:
            sprints = [np.array([orig.strftime("%x"), next_date.strftime("%x")])]
        else:
            sprints += [np.array([orig.strftime("%x"), next_date.strftime("%x")])]
        orig = next_date + timedelta(days=1)

    contributions = np.zeros((len(contributors), 3))

    for i in range(0, len(data)):
        if data[i][2] == "Commit":
            col = 0
        elif data[i][2] == "Issue":
            col = 1
        else:
            col = 2
        row = contributors.index(data[i][0])
        contributions[row][col] += 1

    print(contributions)

    for i in range(0, len(contributors)):
        contributor_report = "User: " + contributors[i]
        if(len(contributor_report) % 2 == 0):
            contributor_report += " "
        space = " "*((len(dash_report) - (len(contributor_report) + 4)) // 2 + 1)
        output.write("%s\n|%s|\n%s\n" % (dash_report, space + contributor_report + space, dash_report))
        output.write("| %s | %s | %s | %s | %s |\n" % (" "*8 +  "Sprint Cycle #" + " "*8, "Number of Contributions", "Number of Commits", "Number of Issues", "Number of Pull Requests"))
        output.write("%s\n" % dash_report)
        for j in range(0, len(sprints)):
            output.write("| Sprint #%0.2d (%s-%s) |" % (j + 1, sprints[j][0], sprints[j][1]))
            output.write(" %d %s |" % (sum(contributions[i]), " "*(22 - len(str(int(sum(contributions[i])))))))
            output.write(" %d %s |" % (contributions[i][0], " "*(18 - len(str(contributions[i][0])))))
            output.write(" %d %s |" % (contributions[i][1], " "*(17 - len(str(contributions[i][1])))))
            output.write(" %d %s |\n" % (contributions[i][2], " "*(24 - len(str(contributions[i][2])))))
            output.write("%s\n" % dash_report)
        output.write("| %s\n" % "Total")
        output.write("%s\n\n%s\n\n" % (dash_report, dash))

    output.write("%s\n" % contributors)
    
    for i in range(0, len(data)):
        index = int(sys.argv[2]) - (contributor_max + 44)
        output.write("| %s | %s | %s | %s |\n" % (data[i][0] + " "*(contributor_max + 1 - len(data[i][0])), data[i][1], data[i][2] + " "*(12 - len(data[i][2])), data[i][3][:index] + " "*(index - len(data[i][3][:index]))))
        if len(data[i][3]) > index:
            data[i][3] = data[i][3][index:]
            while len(data[i][3]) > index:
                output.write("| %s | %s | %s | %s |\n" % (" "*(contributor_max + 1), " "*19, " "*12, data[i][3][:index] + " "*(index - len(data[i][3][:index]))))
                data[i][3] = data[i][3][index:]
        output.write("%s\n" % dash)

if __name__ == '__main__':
    main()
