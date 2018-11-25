# GDET-Fantastic-Four
To test the code, first type the following lines of code into a linux terminal: 
  (1) chmod +x run.sh
  (2) ./run.sh
The above code will first ask (and verify) your GitHub credentials. 

It will then prompt you to input an organization name, followed by a repository name. For example, the Javatrix project can be accessed by typing "JaysGitLab" for the organization name, followed by "cs5666-javatrix-the-fantastic-four" for the repository name. 

The above code will create a directory matching the repository name, which we'll call repo. It'll then create a directory 'repo/data' that stores all the json files curled from the Github API. In particular, this folder will contain 'repo/data/commits' (a directory of all commits), 'repo/data/branches.json', 'repo/data/branches.txt', 'repo/data/contributors.json', 'repo/data/issues.json', and 'repo/data/pulls.json'. These files shouldn't be too interesting after the code finishes compiling, and you may delete the 'repo/data' directory afterwards if you'd like. 

The shell file will pass this information on to the main.py Python file. You will be asked whether you want the report dates to be derived from the earliest to the latest entry. For the Javatrix example, it's best to modify the begin and end dates by typing in "10/15/2018" followed by "11/05/2018". For the sprint cycle length, I'd recommend 7 days. 

The main.py file will then write 2 reports: 
(1) 'repo/student_report.txt': This report contains a summarized report on the contributions of each contributor during all sprints. , and ends with the chronological ordering of all contributions towards the repository. 
(2) 'repo/contribution_report.txt': This report contains all contributions towards the repository in chronological order. These are sorted using the begin/end dates and sprint cycle length inputted earlier. 
