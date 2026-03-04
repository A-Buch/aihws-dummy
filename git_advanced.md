# Advanced commands to survive Git



##  show last commits
`git log --oneline`
* `HEAD`   #  always last commit
* `origin/main and origin/Head`  # reference to remote repo


##  Git merge branch

**Simplest case:**
* fast-forward : no complex merging is need thus can do fast-forward merge


##  Merge commit
* when one branch (e.g. main) is before other branch,
*  merge commit brings "dev" branch back into main

##  Merge conflics
Issue: two branches (e.g. a local branch "dev" and a remote branch "main") have in one or multiple files different versions
1. `git status` # see which file(s) has merge conflict
2. go to each file with merge conflict and solve the areas where you find these arrows: `<<<<` `>>>>` . They indicate where your code differs between local and remote. `incoming` refers to the changes on the remote branch
3. keep either the existing or the incoming part
4. after you solved the conflict for each file, run `git add <fixed-file>`
5. then commit the merge-commit -> "Merge branch 'dev' into main"
6. `git push origin <branch-name,e.g.-dev>`
    - origin : name of default remote repo

###  Alternative: merging via `mergetool` for more complex conflicts
1. install `meld` and add to your git configurations (see,  "Git config settings" section)
2. run `git mergetool`
    - middle : changing part
    - "+" add change, "-" deleting change
<!-- **edit -> accept only current or merging changes** -->
For more info and documentation, see [here](https://git-scm.com/docs/git-mergetool)

#####  Abort merge
* `git merge --abort`



###  Pull from remote branch
* `git pull origin branch_name`

##  Git config settings
* check your Git config settings: `git config --list`
* adapt if needed, eg. username, mail-address
* Optional: Define which tool to use to merge: `git config global mergetool.meld`


## Git - best practice

### General
* For each new development (e.g., a  bug fix or new feature) create a new local and new remote branch

### Errorneous commit
The following is just one potential hack, keep in mind that always multiple solutions exist
1. checkout old commit (before errorneous commit), get the commit id via `git log --oneline`
2. then do changes and delete errorneous commit
3. then make new commit with same name as erroneous commit
-> this deletes errorneous commit without changing history

### Merge branches
Assuming you are on `dev` branch and want to update (ie. merge it to `main`), however, you dont want to mess up anything in the commit history of `main`
Best practice is to solve potential conflicts before doing your merge
1. go to the main branch (or the branch you want to merge into)
2. then merge main branch to your dev branch -> this resolves any potential conflict without messing up "main"
3. then go back to dev and merge back into main (when feature is fully developed / when all conflicts are solved)



## Git - single & multi-person software projects

###  Git Flow (1 person team)
* checkout new branch for each bug and feature
* you can have bug and feature branch simultaneously and then when your are finished merge them back to `main`
* make sure that the `main` branch always works

###  GitFlow (larger teams) [without considering releases]
* have a develop-branch (e.g. called "develop")   simultaneously to your `main` branch and push to regularly new features to "dev"
* bug fixes should be done from `develop` branch by creating new branch and merge it later back to `develop` branch
* Optional: Release branch additional
* After first working version of your software, create a release.
* create first and further releases always from `main`
* When bug is found in `develop` branch - fix there; when found on release branch - fix there


##  Forks
* `git remote add fork git@github.com:attrici.git`
* `git push fork devel`  #  push to my fork, to branch devel
*  `sync fork` #  on webpage to update my fork with the new commits from original repo
<!-- * pull requests are done on webpage fork -> org repo -->

<!-- ######  medium group
#####  skip forks
######  dont trust people:
#####  do protection rules
#####  work with PRs (pull requests) due that test run before -->


<!-- ######  possible to have links similiatnous between forked repo and orignal repo -->



##  Git stash
In case, you want to do some spontaneous stuff in another branch, but you also have undone changes on your current branch --> then use git stash \
Or for the case, you want to move your current changes from one branch to another branch --> then use git stash\
"git stash"  stacks any file you dont want to commit yet, Note: stash is used for short term usage
1. `git stash -m "stashing undone changes in call_api()"`  #  store item(s) with name
2. Do your other stuff eg. change branch
3. `git stash list` #  shows on what commit change set is set
4. `git stash pop @{0}`      #  take id to unstash certain stash, which means apply changes in this stash in your work area
   - alternative: `git stash pop` #  retrieve top element of stack
Further stash commands
* `git stash apply` vs `git stash pop` <-> `git stash apply` does not remove it from stash, other than `git stash pop`
* `git stash drop @{0}` #  remove stash
Show what is in certain stash:
* `git stash show -p @{0}`  #  -p gives patch-form, gives full infos

<!--

##  Git revert commits
#####  revert commit, reverts changeset of this commit, but not removes it from history
#####   but does revert changes on my local git repo, e.g revert commit from: git log --oneline
git show commitname     #  show changes of commit
e.g. git show 3148  #    skip prefix of commit
git revert commitname
git revert HEAD         ###### revert last commit  -->

## Cherry picking with Git :)
Cherry picking means "picking the best things" or certain files from another branch or past commit
 <!-- RELOAD OLD COMMIT  aka cherry pick (pick best thing)
  e.g. implement the changes of a specific (past) commit (form other branch)
#####  creates new commit from old_usefull_commit_from_other_branch
<!-- --> create new commit with same changeset but different parents
<!-- #####  when cherry pick mulitple commit - start with pick oldest commit, then pick next commit -->


##  REBASE  -  tidy up commit history !  (my favorite)

* remove or change commits and their times, --> makes commits more readable
* rebasing: allows to take (multiple) commits and change its parent commit(s) --> allows to reorder commits
*  eg remove unneeded commits (so world dont see them :D)
* `git rebase --interactive HEAD~5`  # 5 = show me last five commits (as i want to change them)
or use
* `git rebase --interactive <commit_hash>`
    -  "pick"  #  this should which commit should be part of the changes
    - remove lines #  drop commits
    - reorder pick-lines #  changing order of commits
    - rename commit
    - squash #  using commit but melting it into previous: !!
        ```
        pick 5719 first commit
        s e00000 commitMessage  #
        s f33033
        ```
    - fixup     #  same as squash but remove all commit messages , better than squash
* Abort git rebase via `--abort`

<!--
TAKE AWAYS
!#  show histroy commits
git log --oneline --graph       #  see commit history
!#  mergetools
git mergetools
- impl merge tools
git pop @{0} or git apply @{0}   #  apply stash and/not remove stash_id from stack
!#  show what is in certain stash
git stash show -p @{0}           #  -p gives patch-form, gives full infos
git show HEAD/commit             #  show changes of commit
!# tidy up commit history, remove unneeded commits
git rebase --interactive <commit_hash>  #  on my dev_branch
#####  -> then do pick xx, fixup xx, s xx (melt commit into previous)
#####  -> then do force push but do this only on my own dev_branch

##  force push
#####  only allowed to use this on my dev_branch
#####  dotn do on main: would skew all people due that their commit history than changes from my rebased  commit history


##  errorneous commits
######  ALTENR 1: when errorneous commit
git revert commitname/HEAD       #  undone changes of commit/lastCommit on repo, but keeps history
######   ALTERN 2: when errorneous commit
#####  checkout old commit (before errorneous commit)
#####  do changes, delete errorneous commit, then make new commit with same name as erroneous commit
#####  -> deletes errorneous commit without changing history



 -->
