import json
import time
import requests
from requests.auth import HTTPBasicAuth


def download_file(url, auth):
    local_filename = "jira-export_{}.zip".format(time.strftime("%Y-%m-%d", time.gmtime()))
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True, auth=auth)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename


JIRA_HOST = "company.atlassian.net"
URL_backup = "https://%(jira_host)s/rest/backup/1/export/runbackup" % {'jira_host': JIRA_HOST}
URL_download = "https://%(jira_host)s/plugins/servlet" % {'jira_host': JIRA_HOST}

auth = HTTPBasicAuth("_user", "_pass")
payload = {"cbAttachments": "true", "exportToCloud": "false"}
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}


def main():
    backup_run = requests.post(URL_backup, data=json.dumps(payload), headers=headers, auth=auth)
    if backup_run.status_code != 200:
        print(backup_run, backup_run.text)
    else:
        task_id = json.loads(backup_run.text)['taskId']
        print('Backup process successfully started ; taskid %s' % task_id)
        URL_progress = "https://%(jira_host)s/rest/backup/1/export/getProgress?taskId=%(task_id)s&_=%(current_ts)s" % \
                       {'jira_host': JIRA_HOST,
                        'task_id': task_id,
                        'current_ts': int(round(time.time() * 1000))
                        }
        time.sleep(10)
        backup_status = {}
        while "result" not in backup_status.keys():
            backup_status = json.loads(requests.get(URL_progress, auth=auth).text)

            print("Current status: {} {}; {}".format(backup_status['status'],
                                                     backup_status['progress'],
                                                     backup_status['description'] + ":" + backup_status['message']
                                                     )
                  )
            time.sleep(120)

        print("Downloading backup file")
        try:
            result = backup_status['result']
            download_file(URL_download + "/%(fileName)s" % {'fileName': result},
                          auth)
        except json.decoder.JSONDecodeError as e:
            print('Something going wrong: %s' % e)
            print('Last data: %s' % backup_status)


if __name__ == '__main__':
    main()
