git stash
git pull origin master
source activate data-analysis
pyinstaller --noconsole -n karlie --distpath ~/Desktop -y karlie/app.py