import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

"""

#app_tables.cache[''] = app_tables.news

@anvil.server.callable
def get_blog_posts():
  return app_tables.blog_posts.search()
  
@anvil.server.callable
def get_blog_post_by_id(i):
  return app_tables.blog_posts.client_writable().get(id=i)
  
@anvil.server.callable
def create_table():
  print('resetting all articles in datatable')
  
  app_tables.articles.delete_all_rows()
  for i in range(1,8):
    app_tables.articles.add_row(id=i, category='Category', title=f'Article {i}', created=datetime.now(),"""
                                #body="""#Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam vulputate massa vitae diam rhoncus, non dictum ante efficitur. Vivamus varius mattis dignissim. Praesent sed metus dui. Vestibulum et augue varius, efficitur est pulvinar, suscipit quam. Vestibulum id magna enim. Etiam interdum arcu viverra malesuada lobortis. Sed porttitor a enim vel congue. Ut vestibulum id risus ac posuere. Nam in lacinia ligula. Sed commodo justo id elit venenatis pretium. Phasellus dictum nunc vel arcu feugiat pellentesque. Aenean vitae turpis placerat, imperdiet lectus at, efficitur erat."""
                               #)