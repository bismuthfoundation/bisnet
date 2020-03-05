#domain system on top of dns, supports both ip valuees and dns entries
#operation:"domain"
#data:"[name]":"[value]"
import tornado.ioloop
import tornado.web
import options
import sqlite3
import webbrowser

config = options.Get()
config.read()
ledger_path = config.ledger_path

connection = sqlite3.connect(ledger_path)
cursor = connection.cursor()

def list_dns():
    cursor.execute("SELECT address, openfield, operation FROM transactions WHERE operation = ? ORDER BY block_height ASC", ("domain",))
    results = cursor.fetchall()

    entry_list = {}
    processed = []
    for entry in results:

        address = entry[0]
        item = entry[1].split(":", 1)
        name = item[0]
        value = item[1]

        if item not in processed: #prevent rewriting
            entry_list[name] = {"value": value, "address": address}
            processed.append(item)

    print(entry_list)
    return entry_list

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("bisnet.html", packed_entries=list_dns())

if __name__ == "__main__":
    app = make_app()
    app.listen(4682)
    webbrowser.open_new_tab("http://127.0.0.1:4682")
    tornado.ioloop.IOLoop.current().start()