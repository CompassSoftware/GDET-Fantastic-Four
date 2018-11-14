read -p "Input GitHub Username: " usrname

read -sp "Input GitHub Password: " pssword

if curl -u $usrname:$pssword https://api.github.com | grep -q "Bad credentials"; then
    echo "Bad credentials. Please try again."
    exit 0
fi 

read -p "Hello $usrname, please input the repository you would like to access. Input in organization/repo format: " repo

contributors="https://api.github.com/repos/$repo/contributors"
commits="https://api.github.com/repos/$repo/commits?page=1&per_page=1000"
issues="https://api.github.com/repos/$repo/issues"
pulls="https://api.github.com/repos/$repo/pulls?state=all"

curl -u $usrname:$pssword $contributors -o contributors.json $commits -o commits.json $issues -o issues.json $pulls -o pulls.json --progress-bar

python3.6 main.py $(tput cols)

cat log.txt
