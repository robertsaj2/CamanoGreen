# CamanoGreen

Developers should pull the latest version of the dev branch and create a branch off of that to do their work.

No branch other than dev should be merged into master.

The development workflow should run as follows:
1. Pull the most recent version of dev
2. Create a branch for the current work
3. When that work is finished, commit to the current branch
4. Checkout dev, and merge the branch containing the work
5. When all proposed changes are finished, merge to master
6. Redeploy master


must set `CG_FLASK_ENV` environment variable to run locally