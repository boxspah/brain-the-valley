from control import Control
from cortex import Cortex
connection_url = "wss://localhost:6868"
user = {
    "client_id": "NZjtUNCOiaPP7gMkNSucchM7jATzNY386Aq2hMI7",
    "client_secret": "526x2Afu46XG6eMMfkJ7Him3QKszzys9Bs4ABKcAVhLa6xfIfSbTs1ZmziBqYcOHWvup3N9XqBo9GbhMAqh2sWSGKQgj5k30PQUwocFaq1haP4eb3oUKMlUp70ZmoOG9",
    "license": "",
    "debit": 500,
}
headset = Cortex(connection_url, user)
main = Control()
main.setup(headset)
main.run_mainloop()
