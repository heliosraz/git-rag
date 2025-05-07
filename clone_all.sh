gh repo list --visibility public | while read -r repo _; do
    gh repo clone "$repo" "$repo"
    echo "Cloned $repo..."
    cd "./$repo"
    git remote remove origin
    rm -rf .git .gitignore .DS_Store .history
    for FILE in $(find . -name "*.py"); do black "$FILE"; done
    echo "Successfully processed $repo..."
    echo "-------------------------------------"
    cd ..
    cd ..
done

