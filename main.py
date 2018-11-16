import json
import sys
import numpy as np

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

def cleanContributors(contributors):
    output = []
    for i in range(0, len(contributors)):
        output.append(contributors[i]['login'])
    return output
    

def cleanCommits(contributors, commits):
    output1 = []
    output2 = []
    output3 = []
    output4 = []
    for i in range(0, len(commits)):
        # Clean committers
        if commits[i]['author'] is not None:
            output1.append(commits[i]['author']['login'])
        elif commits[i]['commit']['author']['name'] in contributors:
            output1.append(commits[i]['commit']['author']['name'])
        else:
            output1.append(stringMetric(commits[i]['commit']['author']['name'], contributors))
        
        # Clean date/time
        output2.append(commits[i]['commit']['author']['date'][:10] + " " + commits[i]['commit']['author']['date'][11:len(commits[i]['commit']['author']['date']) - 1])

        # List of string "Commit"
        output3.append("Commit")
        
        # Clean messages
        output4.append(commits[i]['commit']['message'].replace("\n", " "))
    
    return np.vstack((output1, output2, output3, output4))

def cleanIssues(issues):
    output1 = []
    output2 = []
    output3 = []
    output4 = []
    for i in range(0, len(issues)):
        # Clean committers
        output1.append(issues[i]["user"]["login"])

        # Clean date/time
        output2.append(issues[i]["created_at"][:10] + " " + issues[i]["created_at"][11:len(issues[i]["created_at"]) - 1])
        
        # List of string "Issue"
        output3.append("Issue")

        # Clean messages
        output4.append(issues[i]["title"])
    
    return np.vstack((output1, output2, output3, output4))

def cleanPulls(pulls):
    output1 = []
    output2 = []
    output3 = []
    output4 = []
    for i in range(0, len(pulls)):
        output1.append(pulls[i]["user"]["login"]) 
        output2.append(pulls[i]["created_at"][:10] + " " + pulls[i]["created_at"][11:len(pulls[i]["created_at"]) - 1]) 
        output3.append("Pull Request")
        output4.append(pulls[i]["title"] + " " + pulls[i]["body"])
    
    return np.vstack((output1, output2, output3, output4))

def main():
    # Opens contributors.json, extracts contributor attributes, and puts info into 'contributors'
    with open('contributors.json') as f:
        contributors = json.load(f)
    contributors = cleanContributors(contributors)

    # 'contributor_max'/dash/etc help with formatting table
    contributor_max = 0
    for i in range(0, len(contributors)):
        if len(contributors[i]) > contributor_max:
            contributor_max = len(contributors[i])

    dash = "-"*int(sys.argv[1])
    user = " "*((contributor_max - 4) // 2 + 1) + "User" + " "*((contributor_max - 4) // 2 + 1)
    Date_Time = " "*6 + "Date/Time" + " "*6
    ctype = " "*5 + "Type" + " "*5
    message = " "*((int(sys.argv[1]) - (contributor_max + 48)) // 2 - 1) + "Message" + " "*((int(sys.argv[1]) - (contributor_max + 48)) // 2 - 1)
    
    output = open("log.txt", "w+")
    
    output.write("%s\n" % dash)

    output.write("|%s|%s|%s|%s\n" % (user, Date_Time, ctype, message))

    output.write("%s\n" % dash)
    
    with open('commits.json') as f:
        commits = json.load(f)

    with open('issues.json') as f:
        issues = json.load(f)

    with open('pulls.json') as f:
        pulls = json.load(f)
    
    
    placeholder = np.concatenate((cleanCommits(contributors, commits), cleanIssues(issues), cleanPulls(pulls)), 1)
   
    for i in sorted(range(len(placeholder[1])), key=lambda k: placeholder[1][k], reverse=True):
        index = int(sys.argv[1]) - (contributor_max + 44)
        output.write("| %s | %s | %s | %s\n" % (placeholder[:, i][0] + " "*(contributor_max - len(placeholder[:, i][0])), placeholder[:, i][1], placeholder[:, i][2] + " "*(12 - len(placeholder[:, i][2])), placeholder[:, i][3][:index] + " "*(index - len(placeholder[:, i][3][:index])) + " |"))
        if len(placeholder[:, i][3]) > index:
            placeholder[:, i][3] = placeholder[:, i][3][index:]
            while len(placeholder[:, i][3]) > index:
                output.write("| %s | %s | %s | %s |\n" % (" "*contributor_max, " "*19, " "*12, placeholder[:, i][3][:index]))
                placeholder[:, i][3] = placeholder[:, i][3][index:]
            output.write("| %s | %s | %s | %s |\n" % (" "*contributor_max, " "*19, " "*12, placeholder[:, i][3][:index] + " "*(index - len(placeholder[:, i][3][:index]))))
        output.write("%s\n" % dash)


if __name__ == '__main__':
    main()
