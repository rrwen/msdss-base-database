git init
git add .
git commit -a -m "Initial commit"
git branch -M main
git remote add origin https://github.com/rrwen/msdss-base-database.git
git pull origin main --allow-unrelated-histories
git push -u origin main