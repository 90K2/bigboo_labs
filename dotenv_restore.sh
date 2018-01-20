#!/bin/bash
BACKEND_HOME="/home/user/backend_service_dirs"
BACKUP_DIR="${BACKEND_HOME}/dotenv_backup"


cd $BACKEND_HOME
env_files=$(ls $BACKUP_DIR)
for file in $env_files; do
        yes | cp -rf $BACKUP_DIR/$file $BACKEND_HOME/${file%.env}/.env
done
echo "${#env_files[@]} files saved"