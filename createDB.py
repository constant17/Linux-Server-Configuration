from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Categories, subCategories, Items, Base
import json

engine = create_engine('postgresql://catalog:catalogpw@localhost/appdb')
Base.metadata.bind = engine

# create db sesssion for each group to commit
DBSession = sessionmaker(bind=engine)
session1 = DBSession()
session2 = DBSession()
session3 = DBSession()

data = json.loads(
    open('/var/www/app/app/db_init.json', 'r').read())



try:
	for i in data['categories']:
	    c = Categories(name=i)
	    session1.add(c)
	    session1.commit()

	for i in data['subCategories']:
	    sc = subCategories(
	        category_id=i['category_id'], name=i['name'], description=i['description'])
	    session2.add(sc)
	    session2.commit()

	for i in data['items']:
	    item = Items(name=i['name'], description=i['description'], category=i[
	                 'category'], subCategory=i['subCategory'], price=i['price'])
	    session3.add(item)
	    session3.commit()
	
	session.commit()

except:
	session1.rollback()
	session2.rollback()
	session3.rollback()
	raise RuntimeError('Database write failed.')


print '\nDatabase build successful!'
