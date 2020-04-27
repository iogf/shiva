##############################################################################
# push shiva staging branch.
cd ~/projects/shiva-code
# clean up all .pyc files. 
find . -name "*.pyc" -exec rm -f {} \;
rm -fr ~/projects/shiva-code/static/media
git status
git add *
git commit -a
git push -u origin staging
#############################################################################
# push shiva django-v2 branch.
cd ~/projects/shiva-code
# clean up all .pyc files. 
find . -name "*.pyc" -exec rm -f {} \;
rm -fr ~/projects/shiva-code/static/media
git status
git add *
git commit -a
git push -u origin django-v2
##############################################################################
# push shiva on master.
cd ~/projects/shiva-code
# clean up all .pyc files. 
find . -name "*.pyc" -exec rm -f {} \;

git status
git add *
git commit -a
git push -u origin master
##############################################################################
# merge staging into master.
git checkout master
git merge staging
git push -u origin master
git checkout staging
##############################################################################
# merge master into staging.
git checkout staging
git merge master
git push -u origin staging
git checkout staging

##############################################################################
# merge master into stable.
git checkout stable
git merge master
git push -u origin stable
git checkout master


##############################################################################
# merge alpha into staging.
git checkout staging
git merge alpha
git push -u origin staging
git checkout staging

git branch -d alpha
git push origin :alpha
git fetch -p 

##############################################################################
cd ~/projects/shiva-code
git pull
##############################################################################
# erase database.
cd ~/projects/shiva-code
python manage.py blowdb
./create-superusers
./build-data

python manage.py makemigrations
python manage.py migrate
y
##############################################################################
# stress-db.
./stress-db teta 1
##############################################################################
# create alpha branch.
git checkout -b alpha
git push --set-upstream origin alpha
##############################################################################
# create staging branch.
git checkout -b staging
git push --set-upstream origin staging
##############################################################################
# switch to alpha branch.
git checkout alpha
##############################################################################
# run shiva project.
cd ~/projects/shiva-code
stdbuf -o 0 python manage.py runserver 0.0.0.0:8000
#####k#########################################################################
# create shiva virtualenv.
cd ~/.virtualenvs/
ls -la
# by default, python3 has executable named python in arch linux.
virtualenv shiva -p python
#####k#########################################################################
# activate shiva virtualenv.
cd ~/.virtualenvs/
source shiva/bin/activate
cd ~/projects/shiva-code
##############################################################################
# activate shiva-v2 virtualenv.
cd ~/.virtualenvs/
source shiva-v2/bin/activate
cd ~/projects/shiva-code
##############################################################################
# install shiva dependencies virtualenv.
cd ~/.virtualenvs/
source shiva/bin/activate
cd ~/projects/shiva-code
pip install -r requirements.txt 
##############################################################################
# create shiva project.
cd ~/projects/
django-admin startproject shiva shiva-code
##############################################################################
# create core_app app.
cd ~/projects/shiva-code
python manage.py startapp core_app
##############################################################################
# delete last commit.

cd ~/projects/shiva-code
git reset HEAD^ --hard
git push -f
