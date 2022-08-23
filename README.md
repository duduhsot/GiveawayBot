# GIVEAWAY BOT
[Eng 🇺🇸](https://github.com/dkjfo-lib/Tg_GiveawayBot/blob/main/README.md),
[Rus 🇷🇺](https://github.com/dkjfo-lib/Tg_GiveawayBot/blob/main/README_ru.md)

Telegram bot created for creating and managing giveaways and choosing giveaway winners.

## Commands 

[/g_create   Creates new giveaways.](https://github.com/dkjfo-lib/Tg_GiveawayBot#g_create)

[/g_edit     Changes parameters of a given giveaway.](https://github.com/dkjfo-lib/Tg_GiveawayBot#g_edit)

[/g_subs     Displays subscribed users of a given giveaway.](https://github.com/dkjfo-lib/Tg_GiveawayBot#g_subs)

[/g_post     Creates post about a given giveaway.](https://github.com/dkjfo-lib/Tg_GiveawayBot#g_post)

[/g_finish   Declares winners of a given giveaway.](https://github.com/dkjfo-lib/Tg_GiveawayBot#g_finish)

Only creator of the giveaway can call edit, subs, post and finish commands.

## Deploying to Heroku

1. In config.py file change BOT_TOKEN with bot token from BotFather
1. In config.py file change HEROKU_APP_NAME with app name from Heroku
1. In config.py file make sure LOCAL=False
1. [Deploy app to heroku](https://towardsdatascience.com/how-to-deploy-a-telegram-bot-using-heroku-for-free-9436f89575d2)
1. Check everything deployed correctly
1. It is ready to work

## Commands Description:

### /g_create 
Creates new giveaways.

Arguments:

    - Number of winners
    - Giveaway name
    - Giveaway Description
    - Photo attachment (Optional)

Example:

`/g_create 10''Annal Community Giveaway #11''This time ten lucky subscribers will win a poro plush!`
    

### /g_edit 
Changes parameters of a given giveaway. 

Arguments:

    - Giveaway Id (Is sent to you when new giveaway is created)
    - Number of winners
    - Giveaway name
    - Giveaway Description
    - Photo attachment (Optional) 

Example:

`/g_edit 5a27b099-2d88-4fc4-ac0e-71d7a660a9f9''11''Annal Community Giveaway #11''This time ten lucky subscribers will eleven a poro plush!`

### /g_subs 
Displays subscribed users of a given giveaway. 

Arguments:

    - Giveaway Id (Is sent to you when new giveaway is created)

Example:

`/g_subs 5a27b099-2d88-4fc4-ac0e-71d7a660a9f9`

### /g_post 
Creates post about a given giveaway.

Arguments:

    - Giveaway Id (Is sent to you when new giveaway is created)

Example:

`/g_post 5a27b099-2d88-4fc4-ac0e-71d7a660a9f9`
    
### /g_finish 
Declares winners of a given giveaway.

Arguments:

    - Giveaway Id (Is sent to you when new giveaway is created)

Example:

`/g_finish 5a27b099-2d88-4fc4-ac0e-71d7a660a9f9`

### /restart 
Restarts bot. Works only in LOCAL=True mode