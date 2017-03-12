## TeleBot for managing monitors
###### Bot live @ [t.me/MetropoliaSalesBot](https://t.me/MetropoliaSalesBot)

#### What does this bot do?
This bot is meant to be used by IT staff at universities when they'd like to sell older devices from their storage room, and by students to view lists of those devices and reserve them in advance before purchasing the item at the IT storage room of the university, all using a bot. Since this is supposed to be a fully functional yet a MVP, devices are narrowed down to only `Monitors`.

#### How does it work?
You go to the bot live address mentioned above, and click on `Start`. The button will trigger a `command` (which is `/start`), and from there, you can follow the instructions.

* You start off as a `student` with limited priviliges. Students can only `view` and `reserve` the `Monitors`.
   * Use `/view_monitors` command to see list of monitors in the `stock` (database).
   * Use `/reserve_monitor` command to reserve a monitor by its unique `id`.
* You can use `/admin` command and enter the `SECRET_WORD` to promote yourself from a `student` to an `admin`. `admin`s can do whatever `student`s can do, except `reserve`ing the monitors. You can always use `/student` command to downgrade your priviledges from an `admin` to a `student`. 
   * Use `/add_monitor` command and follow the instructions to add a monitor.
   * Use `/remove_monitor` command to remove a monitor with its unique `id`.
* Use `/me` command to check your public Telegram information + your `admin`/`student` status.
* Finally, use `/help` if need be.

#### Technical implementation
Application is hosted on Heroku, and written with `Python 3.5`. The main script which is run by a `worker` process in Heroku's environment is `bot.py`. There are some rules defined in `Makefile` to simplify my frequent command executions.

#### Licenced under [MIT](https://github.com/Sajjadhosn/telegram_bot_for_IT_sales/blob/master/LICENSE)