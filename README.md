# GDET-Fantastic-Four
To test the code, first type the following lines of code into a linux terminal: 
  (1) chmod +x run.sh
  (2) ./run.sh
The above code will first ask (and verify) your GitHub credentials. 

It will then prompt you to input an organization name, followed by a repository name. For example, the Javatrix project can be accessed by typing "JaysGitLab" for the organization name, followed by "cs5666-javatrix-the-fantastic-four" for the repository name. 

The above code will create a file called 'commits' that stores all json files curled from the Github API. It will also create several json files and store them in the current directory (namely 'contributors.json', 'issues.json', and 'pulls.json'). 

Now the shell file will pass this information on to the main.py Python file. You will be asked whether you want the report dates to be derived from the earliest to the latest entry. For the Javatrix example, it's best to modify the begin and end dates by typing in "10/15/2018" followed by "11/05/2018". 

The main.py file will then write a report to the file 'log.txt', which contains a summarized report on the contributions of each contributor during all sprints, and ends with the chronological ordering of all contributions towards the repository. 
