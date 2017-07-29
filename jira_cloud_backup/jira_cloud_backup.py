import json
import time
import requests
from requests.auth import HTTPBasicAuth


def download_file(url, auth):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True, auth=auth)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename


JIRA_HOST = "company.atlassian.net"
URL_backup = "https://%(jira_host)s/rest/backup/1/export/runbackup" % {'jira_host': JIRA_HOST}
URL_download = "https://%(jira_host)s/plugins/servlet/export/download" % {'jira_host': JIRA_HOST}

auth = HTTPBasicAuth("_user", "_pass")
payload = {"cbAttachments": "true", "exportToCloud": "false"}
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

backup_status = {}

backup_run = requests.post(URL_backup, data=json.dumps(payload), headers=headers, auth=auth)
if backup_run.status_code != 200:
    print(backup_run, backup_run.text)
else:
    print('Backup process successfully started')
    task_id = json.loads(backup_run.text)['taskId']
    URL_progress = "https://%(jira_host)s/rest/internal/2/task/progress/%(task_id)s" % {'jira_host': JIRA_HOST,
                                                                                        'task_id': task_id}
    time.sleep(10)
    backup_status = {}
    while "result" not in backup_status.keys():
        backup_status = json.loads(requests.get(URL_progress, auth=auth).text)

        print("Current status: {} {}; {}".format(backup_status['status'],
                                                 backup_status['progress'],
                                                 backup_status['description']
                                                 )
              )
        time.sleep(300)
print("Downloading backup file")
result = json.loads(backup_status['result'])
download_file(URL_download + "/%(mediaFileId)s/%(fileName)s" % {'mediaFileId': result['mediaFileId'],
                                                                'fileName': result['fileName']},
              auth)
