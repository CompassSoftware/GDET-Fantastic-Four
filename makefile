compile: Node.java LinkedList.java main.java
	$ rm log.txt
	$ curl -i -u hallb2 'https://api.github.com/repos/JaysGitLab/cs5666-javatrix-the-fantastic-four/commits?page=1&per_page=1000' | (grep -E 'name|date|message' | grep -vwE 'payload|"name": "GitHub"') >> log.txt
	javac main.java
	java main
	cat log.txt
