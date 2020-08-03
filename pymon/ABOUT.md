# PyMon - Uptime Monitor

*Disclaimer: I am not an experienced developer and this are my very first steps in Python programming.*

I developed this script because Uptime Robot couldn't reach some of my site's IP, so I needed something that I could run locally without going overpower.

This scripts basically takes a site from a JSON and pings it. If it's down it sends an email to me and my boss.

I want to add some functionallity in the future such as:
* Container reboot when HTTP request is not 200.
* Telegram API integration to send a message instead of an email.
* More reporting (I have commited this, but is not done yet)
* Other responses when a site is down.