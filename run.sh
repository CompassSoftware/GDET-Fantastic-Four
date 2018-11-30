read -p "Input GitHub Username: " usrname
read -sp "Input GitHub Password: " pssword

while curl -u $usrname:$pssword https://api.github.com | grep -q "Bad credentials"
do
    echo "Bad credentials. Please try again (or press ctrl-z to end session)."
    read -p "Input GitHub Username: " usrname
    read -sp "Input GitHub Password: " pssword
done 

read -p "Hello $usrname, input organization: " organization
read -p "Input repository name: " repo

while curl -u $usrname:$pssword https://api.github.com/repos/$organization/$repo | grep -q '"message": "Not Found"'
do
    echo "Incorrect organization/repository name. Please try again (or press ctrl-z to end session)."
    read -p "Hello $usrname, input organization: " organization
    read -p "Input repository name: " repo
done

mkdir $repo
mkdir $repo/data

contributors="https://api.github.com/repos/$organization/$repo/contributors"
branches="https://api.github.com/repos/$organization/$repo/branches"
issues="https://api.github.com/repos/$organization/$repo/issues"
pulls="https://api.github.com/repos/$organization/$repo/pulls?state=all"

curl -u $usrname:$pssword $contributors -o $repo/data/contributors.json $branches -o $repo/data/branches.json  $issues -o $repo/data/issues.json $pulls -o $repo/data/pulls.json --progress-bar

grep "name" $repo/data/branches.json | sed 's/"name": "//' | tr -d ' ' | sed 's/..$//'  > $repo/data/branches.txt

mkdir $repo/data/commits

while IFS= read LINE
do
    mkdir $repo/data/commits/$LINE
    i=1
    
    while :
    do
        curl -u $usrname:$pssword "https://api.github.com/repos/$organization/$repo/commits?page=$i&per_page=100" -o $repo/data/commits/$LINE/commit$i.json
        commit=$repo/data/commits/$LINE/commit$i.json
        if !(grep -q "sha" $commit) then
            rm $repo/data/commits/$LINE/commit$i.json
            break
        fi
        i=$(( $i + 1 ))
    done

done < "$repo/data/branches.txt"



#i=1
#while :
#do
#    curl -u $usrname:$pssword "https://api.github.com/repos/$organization/$repo/commits?page=$i&per_page=100" -o $repo/data/commits/commit$i.json
#    commit=$repo/data/commits/commit$i.json
#    if !(grep -q "sha" $commit) then
#        rm $repo/data/commits/commit$i.json
#        break
#    fi
#    i=$(( $i + 1 ))
#done


python3.6 main.py $repo $(tput cols)

#cat log.txt
