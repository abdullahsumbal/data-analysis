# remove old cloned repos
echo "INFO: removing old repos from download"
rm -Rf ~/Downloads/data-analysis_*
# clone repo
echo "INFO: cloning repo"
repo_folder=~/Downloads/data-analysis_$(date "+%Y.%m.%d-%H.%M.%S")
git clone https://github.com/abdullahsumbal/data-analysis.git --depth 1 $repo_folder

##############################
#Impedance application
##############################

# activate env
echo "INFO impedance: activate env"
source activate impedance
# pip install 
echo "INFO impedance: install requirments"
pip install -r $repo_folder/antranik/requirement.txt
#bake applications
echo "INFO impedance: bake application"
application_name=impedance_$(date "+%Y.%m.%d-%H.%M.%S")
pyinstaller -n $application_name --distpath ~/Desktop/applications --workpath ~/Downloads $repo_folder/antranik/app.py
# clean up
rm -rf ~/Downloads/application_name
rm $application_name.spec
##############################
#karlie application
##############################

# activate env
echo "INFO karlie: activate env"
source activate karlie
# pip install 
echo "INFO karlie: install requirments"
pip install -r $repo_folder/karlie/requirements.txt
#bake applications
echo "INFO karlie: bake application"
application_name=karlie_$(date "+%Y.%m.%d-%H.%M.%S")
pyinstaller --noconsole -n $application_name --distpath ~/Desktop/applications --workpath ~/Downloads $repo_folder/karlie/app.py
# clean up
rm -rf ~/Downloads/application_name
rm $application_name.spec
# copy templates on desktop as well

##############################
#ternary application
##############################

# activate env
echo "INFO ternary: activate env"
source activate ternary
# pip install 
echo "INFO ternary: install requirments"
pip install -r $repo_folder/phase-diagram/requirement.txt
#bake applications
echo "INFO ternary: bake application"
application_name=ternary_$(date "+%Y.%m.%d-%H.%M.%S")
pyinstaller --noconsole -n $application_name --distpath ~/Desktop/applications --workpath ~/Downloads $repo_folder/phase-diagram/app.py
# clean up
rm -rf ~/Downloads/application_name
rm $application_name.spec
# copy templates on desktop as well