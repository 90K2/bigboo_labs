Messrs Moony, Wormtail, Padfoot, and Prongs
Purveyors of Aids to Magical Mischief-Makers
are proud to present
THE MARAUDER'S GITHUB
=============

**yandex_money_http_handler**
-------
- [http_handler](yandex_money_http_handler/http_handler.py) : simple webhook based on bottle microframework. ;
- [transfer_validation](yandex_money_http_handler/transfer_validation.py): check integrity of received payments data ;
- [nginx.conf](yandex_money_http_handler/nginx.conf): one nginx location for redirect Yandex data from front -> python webhook ;

**skype_bot**
-------
- https://apps.dev.microsoft.com/#/appList -- register new app and take `Secret` and `Id` ;
- https://dev.botframework.com/bots        -- create a bot ;

**Usage**: insert your Id/Secret into [skype_sender](skype_bot/skype_sender.py) and call skype_sender:main passing `message` and `skype_id` as argument.
**Important to know**: 
* if you want to send message to the private chat `skype_id` = **skype_login** ;
* if you want to send message to the conversation `skype_id` = **chat_id** ;
                   
How to add skype bot into chat group: you can send message to chat with bot, so that chat will show up in recent chats. Next go to target group and use "Add" button in the top right corner (NOT over group properties) and pick bot from displayed list

How to get skype chat id : just use web version, open target group and filter browser console requests by '@thread' , thread id will be in requests list

**telegram_bot**
-------
- https://core.telegram.org/bots#3-how-do-i-create-a-bot -- just create a new bot and take `TOKEN` ;

**Usage**: pass your `message` and `chat_if` to [tg_sender](telegram_bot/tg_sender.py):main

**Note**: this module is a part of Nagios notification system. So argument `msg_type` allow to insert emodji status into message. Also demonstrated how to use emodji in telegram bot 

**jira_cloud_backup** How to Automate Backups for JIRA Cloud applications
-------

**Usage**: 
- replace `JIRA_HOST` to your "company.atlassian.net" address; 
- insert correct user credentials `auth = HTTPBasicAuth("_user", "_pass")`. **Important**: user must have access to Administration-Backup 

**aws_api**
-------
- [clean_orphaned_snapshots](aws_api/clean_orphaned_snapshots.py) -- search for snapshots without AMI and delete it
- [sign_s3_download_link](aws_api/sign_s3_download_link.py) -- download any s3 file via pre signed direct link without public access

