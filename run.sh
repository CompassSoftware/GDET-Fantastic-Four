read -p "Username:" usrname

curl -u $usrname 'https://api.github.com/repos/JaysGitLab/cs5666-javatrix-the-fantastic-four/contributors' -o contributors.json 'https://api.github.com/repos/JaysGitLab/cs5666-javatrix-the-fantastic-four/commits?page=1&per_page=1000' -o commits.json 'https://api.github.com/repos/JaysGitLab/cs5666-javatrix-the-fantastic-four/commits?page=1&per_page=1000' -o commits.json 'https://api.github.com/repos/JaysGitLab/cs5666-javatrix-the-fantastic-four/commits?page=1&per_page=1000' -o commits.json 'https://api.github.com/repos/JaysGitLab/cs5666-javatrix-the-fantastic-four/commits?page=1&per_page=1000' -o commits.json 'https://api.github.com/repos/JaysGitLab/cs5666-javatrix-the-fantastic-four/commits?page=1&per_page=1000' -o commits.json  'https://api.github.com/repos/JaysGitLab/cs5666-javatrix-the-fantastic-four/commits?page=1&per_page=1000' -o commits.json 'https://api.github.com/repos/JaysGitLab/cs5666-javatrix-the-fantastic-four/issues' -o issues.json

python main.py $(tput cols)

cat log.txt
