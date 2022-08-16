from ._anvil_designer import MainTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
routing.logger.debug = True # Toggle this setting for logging print statements

from ..Admin import Admin
from ..ArticleForm import ArticleForm
from ..ListArticlesForm import ListArticlesForm
from ..error_form import error_form
from ..Home import Home
from ..BlogPostForm import BlogPostForm
from ..ListBlogPostsForm import ListBlogPostsForm
from ..Contact import Contact
from ..Library import Library
from ..User import User

"""anvil.server.call('create_table')"""

@routing.main_router
class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Load username on profil
    user = anvil.server.call('get_user')
    self.user_link.text = str(user['email'])[0:int(str(user['email']).find('@'))] 
    
    self.links = [self.articles_link,
                  self.blog_posts_link,
                  self.admin_link,
                  self.contact_link,
                  self.library_link,
                  self.user_link]
    
    self.home_link.tag.url_hash = 'home'
    self.blog_posts_link.tag.url_hash = 'blog-posts'
    self.articles_link.tag.url_hash = 'articles'
    self.admin_link.tag.url_hash = 'admin'
    self.contact_link.tag.url_hash = 'contact'
    self.library_link.tag.url_hash = 'library'
    self.user_link.tag.url_hash = 'user'
    
  """
  QUERY
  """
  
  # Search labels from data table
  def get_label(self, label, **event_args):
    return list(set([str(row[label]) for row in app_tables.labels.search()]))[:-1]
  
  # Search dates from data table
  def get_date(self, format, order, **event_args):
    return list(set([row['created'].strftime(format) for row in app_tables.contacts.search(
      tables.order_by(order,ascending = False))]))

  # ???
  def on_navigation(self, **nav_args):
    # this method is called whenever routing navigates to a new url
    # an example of setting the link as selected 
    # depending on the url_hash that is being navigated to
    for link in self.links:
      link.role = 'selected' if link.tag.url_hash == nav_args['url_hash'] else ''
  
  """
  LINK
  """

  # ???
  def nav_link_click(self, **event_args):
    """This method is called when a navigation link is clicked"""
    url_hash = event_args['sender'].tag.url_hash
    routing.set_url_hash(url_hash)

  # ???
  def refresh_click(self, **event_args):
    """This method is called when the button is clicked"""
    routing.reload_page()

  # ???
  def logout_link_click(self, **event_args):
    anvil.users.logout()
    open_form('Login')