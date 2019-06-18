rm -rf ~/data-analysis/
git clone https://github.com/abdullahsumbal/data-analysis.git ~/data-analysis
cd ~/data-analysis
source activate data-analysis
pyinstaller --noconsole -n karlie --distpath ~/Desktop -y karlie/app.py