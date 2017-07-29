Messrs Moony, Wormtail, Padfoot, and Prongs
Purveyors of Aids to Magical Mischief-Makers
are proud to present
THE MARAUDER'S GITHUB
=============

**yandex_money_http_handler**
-------
- http_handler : simple webhook based on bottle microframework. 
- transfer_validation: check integrity of received payments data
- nginx.conf: one nginx location for redirect Yandex data from front -> python webhook 

**skype_bot**
-------
- https://apps.dev.microsoft.com/#/appList -- register new app and take `Secret` and `Id`
- https://dev.botframework.com/bots        -- create a bot

**usage**: insert your Id/Secret into [skype_sender](https://github.com/90K2/bigboo_labs/blob/master/skype_bot/skype_sender.py) and call skype_sender:main passing `message` and `skype_id` as argument.
**important to know**: 
* if you want to send message to the private chat `skype_id` = **skype_login**
* if you want to send message to the conversation `skype_id` = **chat_id**
                   
I spent many a lot of time searching how to find out this f**g `chat_id`. Very simple: enter **/get name** in conversation :simple_smile:
