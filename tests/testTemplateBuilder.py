from context import dbhandler


class testdb:

    def testdb():
        table = dbhandler.getDebugDB()
        type = "testwerktniet"
        item = table.get_item(Key={'Type': "temp"})
        print(item)


testdb.testdb()
