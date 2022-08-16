import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

app_tables.cache[''] = app_tables.articles

@anvil.server.callable
def get_articles():
  return app_tables.articles.client_writable().search()

@anvil.server.callable
def get_blog_posts():
  return app_tables.blog_posts.search()

@anvil.server.callable
def get_emails():
  return app_tables.contacts.search()

@anvil.server.callable
def get_article_by_id(i):
  i = int(i)
  return app_tables.articles.client_writable().get(id=i)

@anvil.server.callable
def get_blog_post_by_id(i):
  return app_tables.blog_posts.client_writable().get(id=i)

@anvil.server.callable
def get_emails_by_id(i):
  return app_tables.contacts.client_writable().get(id=i)

@anvil.server.callable
def create_table():
  print('resetting all articles in datatable')
  
  app_tables.articles.delete_all_rows()
  for i in range(1,8):
    app_tables.articles.add_row(id=i, category='Category', title=f'Article {i}', created=datetime.now(),
                                body="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam vulputate massa vitae diam rhoncus, non dictum ante efficitur. Vivamus varius mattis dignissim. Praesent sed metus dui. Vestibulum et augue varius, efficitur est pulvinar, suscipit quam. Vestibulum id magna enim. Etiam interdum arcu viverra malesuada lobortis. Sed porttitor a enim vel congue. Ut vestibulum id risus ac posuere. Nam in lacinia ligula. Sed commodo justo id elit venenatis pretium. Phasellus dictum nunc vel arcu feugiat pellentesque. Aenean vitae turpis placerat, imperdiet lectus at, efficitur erat."""
                               )

@anvil.server.callable
def create_new_article():
  rows = app_tables.articles.search(tables.order_by('id',ascending=False))
  
  if len(rows):
    last_id = rows[0]['id']  + 1
  else:
    last_id = 1
  
  return app_tables.articles.client_writable().add_row(id=last_id, category='Category', title=f'Article {last_id}', created=datetime.now(),
                                body="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam vulputate massa vitae diam rhoncus, non dictum ante efficitur. Vivamus varius mattis dignissim. Praesent sed metus dui. Vestibulum et augue varius, efficitur est pulvinar, suscipit quam. Vestibulum id magna enim. Etiam interdum arcu viverra malesuada lobortis. Sed porttitor a enim vel congue. Ut vestibulum id risus ac posuere. Nam in lacinia ligula. Sed commodo justo id elit venenatis pretium. Phasellus dictum nunc vel arcu feugiat pellentesque. Aenean vitae turpis placerat, imperdiet lectus at, efficitur erat."""
                               )

#Contact
@anvil.server.callable
def add_row(user, category, subject, message):

  app_tables.contacts.add_row(id = app_tables.contacts.search(tables.order_by('id', ascending=False))[0]['id'] + 1 ,
                              email = user,
                              created = datetime.now(),
                              month_order = datetime.now().month,
                              month = datetime.now().strftime('%B'),
                              year = datetime.now().year,
                              category = category,
                              subject= subject,
                              message = message,
                              status = False
                             )

@anvil.server.callable
def delete_row(row):
  # check that the row being deleted exists in the Data Table
  if app_tables.contacts.has_row(row):
    row.delete()
  else:
    raise Exception("Article does not exist")
    
@anvil.server.callable
def update_row(row, value):
  # check that the row being deleted exists in the Data Table
  if app_tables.contacts.has_row(row):
    row.update(status = value)
  else:
    raise Exception("Article does not exist")

# Main / Contact
# Get user from data table
@anvil.server.callable
def get_user():
  return app_tables.users.get(email = anvil.google.auth.get_user_email())

# Get labels from data table
@anvil.server.callable
def get_label(label):
  return list(set([str(row[label]) for row in app_tables.labels.search()]))[:-1]
  
# Get dates from data table
@anvil.server.callable
def get_date(format, order):
  return list(set([row['created'].strftime(format) for row in app_tables.contacts.search(
    tables.order_by(order,ascending = False))]))