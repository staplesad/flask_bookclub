from bookclub_app import db, models

#set up a couple of database entries so that the website will start without errors

db.create_all()
exampleUser = models.User("example", "example@emailaddress.com", "password")
singleQuote = models.Quote(quote_text = "This is a very literary quote")
db.session.add(exampleUser)
db.session.add(singleQuote)
db.session.commit()

