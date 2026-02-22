# Basic commands to survive git
Private file to do handson session



## Start a new repository


### 1. Init new repository
`$ git init` 	# initialize (empty) git repo from my curr wd

ls .git		# contains config etc , dot in front of file means it is for system, .git indicates that its parent folder is a git directory

### 2. create first python_file 
`$ nano python_file.py` 	# make file or use `vim` instead of `nano` etc. 

### 3. Git add & staging & committing:
Use `git add, git commit` when did changes to file


`$ git add python_file`  # add files that should be committed
`$ git add subdir/` 	# add entire subdir, not recommended as easily include also .cache folder etc

`$ git rm -frn <foldername/filename>`   # force remove, do it recursively and as dry-run 


`$ git commit -m "add short explanation about changes in the file(s)"`	# commit file to tree
Alternative (less recommended): `$ git commit`	  
    - in nano-mode: write commit, then exit: `:qa!` + Enter \
Advanced usage:
- `$ git commit -m "feat(hpc): add short explanation, issue: #commit_hash"` # when working with issues
- `$ git commit -m "feat(hpc): add short explanation"  -- file_1_to_commit file_2_to_commit`  # commit only certain file(s)
- `$ git commit -m "feat(hpc): add short explanation" -m "* more detailed explanation 1" -m "* more detailed explanation 2"   -- file_1_to_commit file_2_to_commit`  # provide further info about commit (usually as a list)

`$ git status`	# shows what current state of branches
    - red: shows files which are not under version control
    - green: files which will be committed 


`$ git log` 	# shows history of all files
- Recommended alternative: `$ git log --oneline --graph`
    - HEAD: always last commit <unique hash is identified also by head> 	
    - Shows hash code - uniquely, always use to commit file <in cmd information>

`$ git show commit_hash`  # shows what is in commit
- always refer to commit by using its hash, called also SHA-1 or SHA



#### Secret files/folders
Exclude certain folders/files from commit\
`$ nano .gitignore`

Suggestions what i usually include in `.gitingore`

```
# config and cache files
__pycache__/
.ipynb_checkpoints/
.pytest_cache/
.ruff_cache/
.env   # e.g., stores private access tokens


# uv (or any other package manager like conda or pip venv)
.venv/
uv.lock

# stored models and models configs
*.pkl

optional: logs and merge tool orig files
*.orig  # automatic backups created by `$ git during merge conflict

# Optional: Do not ignore specific files/folders but all 
other files/folder with same pattern
    # Example 1
    # Ignore notebooks, except specific ones needed for calibrating model interactively
    *.ipynb
    !bayesian-network/*.ipynb

    # Example 2
    # Dont ignore test data when identically named folder exists
    input/
    !tests/test_data/input
```
- `$ git add .gitignore`
- `$ git commit -m "build(gitignore): init .gitignore"` -- .gitignore
- `$ git status`  # shows now only non-secret files/folders
- `$ git status --ignored` 	# shows ignored files
- Templates for `.gitignore` files exists online for each programming language. Benefit: they include all system packages related to specific programming language

**NOTE:**\
*"If you already have a file checked in, and you want to ignore it, Git wont ignore the file if you add a rule later. In those cases, you must untrack the file first, by running the following command: `$ git rm --cached FILENAME`"*



**NOTE:**\
**Store logs and data folders (except test data) better outside of repo**


### 4. Git push
Before pushing:
- `$ git branch`   # shows current branch\
- `$ git branch -v`  # shows all local and remote branches\
- `$ git remote -v`  # verify that we push to the correct repo

When pushing to remote repo:
- `$ git push`
Push alternatives:

-  `$ git push origin local_branchname:remote_branchname` # push to another branch
    - `origin` #  reference to remote repo
    


### 5. Difference between file versions
`$ git diff file.py`     # compare file versions older vs. newer
- compares working directory with staging area
- @@ shows line that was changedQ
- green text: shows what added, red text: what was removed

`$ git diff --staged file.py` # compare repo with working copy (i.e., file is in staging area)

#### Staging area
- Staging area is an intermediated instance between the local PC and the remote repo. If the staging area would not exist then temporary changes would be also added to remote repo (<-- and we usually dont want this)

    ![alt text](git_staging.png)(Figure: Description about staging area.)

`$ git diff HEAD file.py` 	# similar to `$ git diff file.py`
`$ git diff HEAD~1 file.py` # show changes to second last commit 

`$ git checkout HEAD file.py` # go back before python.py in repo 
- therefore no python file anymore in `$ git status`	# go to HEAD 
- does not change repo


#### Removing previous commits
Undo last commit (before pushed commit), then check with `git status` if the working copy is clean:\
`$ git reset --soft HEAD` or simply `$ git reset HEAD~1` 

Undo last commit and completely remove all changes:\
`$ git reset --hard HEAD~1` <maybe leave out this command as I have not used it regularly, similar to git revert HEAD>


### 6. Branches
`$ git checkout -b feat-branch` 	# switch/create new branch

Most common branch types:
- `main`-branch: 
    - Most recent working version of the code which should work without throwing errors ;) 
    - Former called `master`
    - colleagues, users etc. will use this version  
- `feature`-branches: 
    - Add a new feature of the project
    - Development area (at least in smaller projects) where you usually work
    - Preferably colleagues should not use this branch without letting you know (because of `git rebase`)
- `fix`-branches: Debug an existing branch
- `dev`-branch: 
    - Only common in larger (multi-developer) software projects. It is a branch between `main` and `feature`-branches
    - Used to merge feature-branches together so the team can test their entire software before pushing it to `main`. In other words, this branch is an additional layer to ensure that always a working version of the software is on `main`.



## Helpful commands

`$ git xxx --help`   # see options for certain command  
- Example: `$ git config -h`  # setup git configurations

`$ touch filename`	 # if it does not exists -> create file


