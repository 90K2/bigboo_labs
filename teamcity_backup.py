import requests
from bs4 import BeautifulSoup
from datetime import datetime

TC_URL = "teamcity address"
TC_TOKEN = "tc api token"

headers = {"Authorization": "Bearer %s" % TC_TOKEN}


def get_tc_version():
    r = requests.get(TC_URL + "/login.html")
    soup = BeautifulSoup(r.text, "html.parser")
    v_raw = soup.findAll("span", {"class": "greyNote version"})
    return v_raw[0].contents[1]


def main():
    current_version = get_tc_version()
    # backup_name = "TeamCity_Backup_%s_%s" % (current_version.replace(" ", "_"), datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S"))
    backup_name = "TeamCity_Backup_%s_%s" % current_version.replace(" ", "_")

    r = requests.post(TC_URL + "/app/rest/server/backup",
                      params={"includeConfigs": True,
                              "includeDatabase": True,
                              "fileName": backup_name
                              },
                      headers=headers
                      )
    print(r.text)
    print(r.status_code)

    r = requests.get(TC_URL + "/app/rest/server/backup",
                     headers=headers
                     )
    print(r.text)  # Running | Idle


if __name__ == '__main__':
    main()
