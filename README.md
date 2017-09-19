# counterUAV

## How to download this repository

In a terminal, do following command in where you want to create git repository.
For example, in /home/User/repo, do:
```
git clone git@github.com:seonghapark/counterUAV.git
```
Then a folder named counterUAV will be created. After that, create your own branch and upload your works. 
Master branch is a basically provided git repository where we will not use for this project. 

## How to create your branch
In the git repository do following command:
```
git checkout -b <your branch name>
```
For example:
```
git checkout -b spark
```
Then you will have your branch with your branch name.
To check the branch where you are, do:
```
git branch
```

To change branch, do:
```
git checkout <branch name>
```
For example,
```
git checkout spark
git checkout master
```

## How to download data
To download all the data in a git repository, do:
```
git pull
```
If you did not specify a git branch, this will download all data where you are now. 
If you want to download data to your git repository from other git repository, do:
```
git pull origin spark
git pull origin master
```
## How to upload data
To upload all the data, use following commands at the top level of your git repository:
```
git status                                        To check the changes in the repository
git add --all *                                   Add all changes in the repository on a commit list
git commit -m "<comments about this upload">      Get commit number and commit changes
git push                                          Upload data
```
## !!! Be cautious not to screw other git repository !!!
Before you upload data, do```git pull```first at anytime.


## How to ignore all the changes in a repository
use
```
git reset hard
```
This command will remove all changes in your git repository.
