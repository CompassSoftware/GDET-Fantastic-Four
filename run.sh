read -p "Input GitHub Username: " usrname

read -sp "Input GitHub Password: " pssword

if curl -u $usrname:$pssword https://api.github.com | grep -q "Bad credentials"; then
    echo "Bad credentials. Please try again."
    exit 0
fi 

read -p "Hello $usrname, input organization: " organization
read -p "Input repository name: " repo

mkdir $repo
mkdir $repo/commits

i=1
while :
do
    curl -u $usrname:$pssword "https://api.github.com/repos/$organization/$repo/commits?page=$i&per_page=100" -o $repo/commits/commit$i.json
    commit=$repo/commits/commit$i.json
    if !(grep -q "sha" $commit) then
        rm $repo/commits/commit$i.json
        break
    fi
    i=$(( $i + 1 ))
done

contributors="https://api.github.com/repos/$organization/$repo/contributors"
issues="https://api.github.com/repos/$organization/$repo/issues"
pulls="https://api.github.com/repos/$organization/$repo/pulls?state=all"

curl -u $usrname:$pssword $contributors -o $repo/contributors.json $issues -o $repo/issues.json $pulls -o $repo/pulls.json --progress-bar

python3.6 main.py $repo $(tput cols)

#cat log.txt
