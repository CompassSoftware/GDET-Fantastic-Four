import json
import sys
import numpy as np
import os
import datetime
from datetime import timedelta

# 'repo' represents the repository name requested by the user. 
# 'width' represents the character width of the terminal. 
# 'dash' represents the horizontal borders of various tables. 
repo = sys.argv[1]
width = int(sys.argv[2])

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
        return "*"

def cleanContributors(contributors):
    output = np.array([])

    for i in range(0, len(contributors)):
        output = np.append(output, contributors[i]['login'])

    return output

def cleanCommits(contributors, branch):
    output = np.array([])

    for filename in os.listdir(repo + '/data/commits/' + branch):
        with open(repo + '/data/commits/' + branch + '/' + filename) as f:
            commits = json.load(f)
            temp = np.zeros((len(commits), 4), dtype=object)
    
            for i in range(0, len(commits)):
                # Clean committers
                if commits[i]['author'] is not None:
                    temp[i][0] = commits[i]['author']['login']
                elif commits[i]['commit']['author']['name'] in contributors:
                    temp[i][0] = commits[i]['commit']['author']['name']
                else:
                    temp[i][0] = stringMetric(commits[i]['commit']['author']['name'], contributors)

                # Clean date/time
                temp[i][1] = commits[i]['commit']['author']['date'][:10] + " " + commits[i]['commit']['author']['date'][11:len(commits[i]['commit']['author']['date']) - 1]

                # List of string "Commit"
                temp[i][2] = "Commit"

                # Clean messages
                temp[i][3] = commits[i]['commit']['message'].replace('\r', '').replace('\t', '').replace('\n', '.')

            if output.size == 0:
                output = temp
            else:
                output = np.vstack((output, temp))
   
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
        # Clean committers
        output[i][0] = pulls[i]["user"]["login"]
        
        # Clean date/time
        output[i][1] = pulls[i]["created_at"][:10] + " " + pulls[i]["created_at"][11:len(pulls[i]["created_at"]) - 1]
        
        # List of string "Pull Request"
        output[i][2] = "Pull Request"

        #Clean messages
        output[i][3] = (pulls[i]["title"] + " " + pulls[i]["body"]).replace('\n', '').replace('\r', '')

    return output

# Centers a string s based off of character width n
def center(s, n, default = False):
    if n == width and default == False:
        space = " "*((n - len(s)) // 2)
    else:
        space = " "*((n - len(s)) // 2 - 1)
    
    output = space + s + space
    
    if len(output) + 2 != n:
        return output + " "
    else:
        return output

def dashes(length, textfile):
    if length == width:
        textfile.write("-"*length)
        textfile.write('\n')
    else:
        textfile.write("%s\n" % center("-"*length, width))

def title(s, textfile):
    dashes(width, textfile)
    textfile.write("%s\n" % center(s, width))
    dashes(width, textfile)

def header(headings, length, textfile, default = False):
    try:
        headings.isalpha
        dashes(length, textfile)
        textfile.write("%s\n" % center("|%s|" % center(headings, length, default), width))
        dashes(length, textfile)
    
    except AttributeError:
        for heading in headings:
            dashes(length, textfile)
            textfile.write("%s\n" % center("|%s|" % center(heading, length, default), width))
        dashes(length, textfile)

def contributorMax(contributors):
    contributor_max = 0

    for contributor in contributors:
        if len(contributor) > contributor_max:
            contributor_max = len(contributor)

    return contributor_max

class Cleaner(object):

    def __init__(self):
        Cleaner.data = np.array([])
        Cleaner.sprints = np.array([])
        
        with open(repo + '/data/contributors.json') as f:
            Cleaner.contributors = cleanContributors(json.load(f))

        Cleaner.contributor_max = contributorMax(Cleaner.contributors)

        Cleaner.index = width - (Cleaner.contributor_max + 44)

        with open(repo + '/data/issues.json') as f:
            Cleaner.data = cleanIssues(json.load(f))            

        with open(repo + '/data/pulls.json') as f:
            Cleaner.data = np.vstack((Cleaner.data, cleanPulls(json.load(f))))

        Cleaner.commits = np.array([])

        for branch in os.listdir(repo + '/data/commits'):
            if Cleaner.commits.size == 0:
                Cleaner.commits = cleanCommits(Cleaner.contributors, branch)
            else:
                Cleaner.commits = np.vstack((Cleaner.commits, cleanCommits(Cleaner.contributors, branch)))
        
        Cleaner.data = np.unique(np.array(np.vstack((Cleaner.data, Cleaner.commits)), dtype=str), axis=0)

        temp = Cleaner.data

        Cleaner.data = np.array([])

        for i in sorted(range(len(temp[:, 1])), key=lambda k: temp[:, 1][k], reverse=True):
            if Cleaner.data.size == 0:
                Cleaner.data = temp[i]
            else:
                Cleaner.data = np.vstack((Cleaner.data, temp[i]))

    def sprintCycles(self):
        orig = datetime.datetime.strptime(Cleaner.data[len(Cleaner.data) - 1][1][:10], '%Y-%m-%d')
        fin = datetime.datetime.strptime(Cleaner.data[0][1][:10], '%Y-%m-%d')
    
        # Prompts user to choose begin/end dates of report, or defaults to first/last contribution if (n) is chosen. 
        choice = input("Earliest contribution is " + orig.strftime('%x') + " and latest contribution is " + fin.strftime('%x') + ". Would you like to change these dates in the report? (Enter y/n) ")
    
        while choice != 'y' and choice != 'n':
            choice = input("Incorrect input. Please enter (y) to change dates, or (n) to keep dates. ")
   
        if choice == 'y':
            while True:
                try:
                    orig = datetime.datetime.strptime(input("Please enter beginning date: (mm/dd/yyyy Format) "), '%m/%d/%Y')
                    fin = datetime.datetime.strptime(input("Please enter end date: (mm/dd/yyyy Format) "), '%m/%d/%Y')
                    break
                except ValueError:
                    print("Dates entered do not match form mm/dd/yyyy. Please try again.")

        # User inputs sprint cycle duration, and each sprint cycle is recorded and stored in 'sprints'
        sprint_cycle = int(input("Please enter sprint cycle length: (in days) ")) - 1

        while orig <= fin:
            next_date = orig + timedelta(days = sprint_cycle)
        
            if len(Cleaner.sprints) == 0:
                Cleaner.sprints = [np.array([orig, next_date])]
            else:
                Cleaner.sprints += [np.array([orig, next_date])]

            orig = next_date + timedelta(days=1)

class userContributions(Cleaner):
    
    def __init__(self, user):
        self.user = user
        self.contributions = np.zeros((len(Cleaner.sprints) + 1, 4), dtype=int)
    
    def numOfContributions(self):
        for i in range(0, len(Cleaner.sprints)):
            for j in range(0, len(Cleaner.data)):
                if str(Cleaner.sprints[i][0]) <= Cleaner.data[j][1] and str(Cleaner.sprints[i][1] + timedelta(seconds = -1, days = 1)) >= Cleaner.data[j][1] and Cleaner.data[j][0] == self.user:
                    if Cleaner.data[j][2] == "Commit":
                        self.contributions[i][1] += 1
                    elif Cleaner.data[j][2] == "Issue":
                        self.contributions[i][2] += 1
                    else:
                        self.contributions[i][3] += 1
        
        for i in range(0, len(Cleaner.sprints)):
            self.contributions[i][0] = sum(self.contributions[i])

        for i in range(0, 4):
            self.contributions[len(Cleaner.sprints)][i] = sum(self.contributions[:len(self.contributions) - 1, i])

    def studentReport(self, textfile):
        sprint_cycle = center("Sprint Cycle #", len("| Sprint #01 (mm/dd/yy-mm/dd/yy) |"))
        number_of_contributions = center("Number of Contributions", len("| Number of Contributions |"))
        number_of_commits = center("Number of Commits", len("| Number of Commits |"))
        number_of_issues = center("Number of Issues", len("| Number of Issues |"))
        number_of_pulls = center("Number of Pull Requests", len("| Number of Pull Requests |"))
        temp = "%s|%s|%s|%s|%s" % (sprint_cycle, number_of_contributions, number_of_commits, number_of_issues, number_of_pulls)

        header(("User: " + self.user, temp), 125, textfile)
        
        for i in range(0, len(self.contributions)):
            if i != len(self.contributions) - 1:
                sprint_cycle = "| Sprint #%0.2d (%s-%s) " % (i + 1, Cleaner.sprints[i][0].strftime('%x'), Cleaner.sprints[i][1].strftime('%x'))
            
            else:
                sprint_cycle = "|" + center("Total", len("Sprint #01 (mm/dd/yy-mm/dd/yy)") + 4)
            
            number_of_contributions = "|" + center(str(self.contributions[i][0]), len("| Number of Contributions |"))
            number_of_commits = "|" + center(str(self.contributions[i][1]), len("| Number of Commits |"))
            number_of_issues = "|" + center(str(self.contributions[i][2]), len("| Number of Issues |"))
            number_of_pulls = "|" + center(str(self.contributions[i][3]), len("| Number of Pull Requests |")) + "|"
            textfile.write("%s\n" % center(sprint_cycle + number_of_contributions + number_of_commits + number_of_issues + number_of_pulls, width)) 
            dashes(125, textfile)

class Contributions(Cleaner):

    def __init__(self):
        pass

    def contributionReport(self, textfile):
        # 'sprint_header' is the heading used for each sprint cycle
        user = center("User", Cleaner.contributor_max + 4)
        date_time = center("Date/Time", len("| yyyy-mm-dd hh:mm:ss |"))
        ctype = center("Type", len("| Pull Request |"))
        message = center("Message", Cleaner.index + 3)
        sprint_header = "%s|%s|%s|%s" % (user, date_time, ctype, message)
    
        for i in range(0, len(Cleaner.sprints)):
            sprint_cycle = "Sprint #%0.2d (%s-%s)" % (i + 1, Cleaner.sprints[i][0].strftime('%x'), Cleaner.sprints[i][1].strftime('%x'))
            header((sprint_cycle, sprint_header), width, textfile, True)
            for j in range(len(Cleaner.data) - 1, -1, -1):
                if str(Cleaner.sprints[i][0]) <= Cleaner.data[j][1] and str(Cleaner.sprints[i][1] + timedelta(seconds = -1, days = 1)) >= Cleaner.data[j][1]:
                    user = "|" + center(Cleaner.data[j][0], Cleaner.contributor_max + 4)
                    date_time = "|" + center(Cleaner.data[j][1], len("yyyy-mm-dd hh:mm:ss") + 4)
                    ctype = "|" + center(Cleaner.data[j][2], len("Pull Request") + 4)
                    message = "| " + Cleaner.data[j][3][:Cleaner.index]
                    message = message + " "*(Cleaner.index - len(message) + 2) + " |"
                    textfile.write("%s\n" % center(user + date_time + ctype + message, width))

                    while len(Cleaner.data[j][3]) > Cleaner.index:
                        Cleaner.data[j][3] = Cleaner.data[j][3][Cleaner.index:]
                        textfile.write("|%s|%s|%s| %s|\n" % (center("", Cleaner.contributor_max + 4), center("", len("yyyy-mm-dd hh:mm:ss") + 4), center("", len("Pull Request") + 4), Cleaner.data[j][3][:Cleaner.index] + " "*(Cleaner.index - len(Cleaner.data[j][3][:Cleaner.index]) + 1)))

                    dashes(width, textfile)   

            textfile.write("\n%s\n\n" % ("%"*width))

def main():
    data = Cleaner()
    data.sprintCycles()

    # Creates a text file called "student_record", and subsequently makes a title. 
    student_report = open(repo + "/student_report.txt", "w+")
   
    title("Student Report for " + repo, student_report)

    student_report.write("\n%s\n\n" % ("%"*width))

    # Writes and formats all information to student_record.txt. 
    for user in data.contributors:
        c = userContributions(user)
        c.numOfContributions()
        c.studentReport(student_report)
        student_report.write("\n%s\n\n" % ("%"*width))
    
    student_report.close()
 
    # Creates a text file that will record all contribution records and subsequently creates a header.
    contribution_report = open(repo + "/contribution_report.txt", "w+")

    title("Contribution Report for " + repo, contribution_report)

    contribution_report.write("\n%s\n\n" % ("%"*width))

    d = Contributions()

    d.contributionReport(contribution_report)
    
    contribution_report.close()


if __name__ == '__main__':
    main()
