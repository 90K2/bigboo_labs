#!/bin/bash
BACKEND_HOME="/home/user/backend_service_dirs"
BACKUP_DIR="${BACKEND_HOME}/dotenv_backup"

if [ -d "${BACKUP_DIR}" ]; then
        rm -rf $BACKUP_DIR
fi
mkdir $BACKUP_DIR

cd $BACKEND_HOME
repo_list=$(ls -d */)
for repo in $repo_list; do
        cp $repo.env $BACKUP_DIR/${repo%/}.env
done
echo "${#repo_list[@]} files saved"