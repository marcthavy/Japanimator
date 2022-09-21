from ._anvil_designer import MainTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..Administration.Inbox import Inbox
from ..Administration.Inbox.EmailForm import EmailForm
from ..Administration.Tags import Tags
from ..Administration.User import User

from ..Collection import Collection
from ..Collection.AnimeForm import AnimeForm
from ..Contact import Contact
from ..Home import Home
from ..Login import Login
from ..News import News
from ..News.ArticleForm import ArticleForm
from ..UserForm import UserForm
from ..error_form import error_form

from HashRouting import routing
routing.logger.debug = True # Toggle this setting for logging print statements

@routing.main_router
class Main(MainTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Set variables (callable from children)
    self.user = anvil.server.call('get_user') #anvil.users.get_user()
    self.date_format = 'dd/mm/YY à HH:MM:SS'
    self.error = '1px solid red'
    self.valid = '1px solid green'
    self.bgcolor = '#FAFAFA'
    
    # Load username on user_link
    self.user_link.text = str(self.user['email'])[0:int(str(self.user['email']).find('@'))]
    
    # Show privilege admin access
    if self.user['admin']:
      self.inbox_link.visible = True
      self.tag_link.visible = True
      self.users_link.visible = True
    else:
      self.inbox_link.visible = False
      self.tag_link.visible = False
      self.users_link.visible = False
    
    # Set url_hash on links
    self.links = [
      self.inbox_link,
      self.tag_link,    
      self.users_link,  
      self.collection_link,
      self.contact_link,
      self.home_link,
      self.news_link,
      self.user_link
    ]
    
    self.inbox_link.tag.url_hash = 'inbox'
    self.tag_link.tag.url_hash = 'tag'
    self.users_link.tag.url_hash = 'users'
    self.collection_link.tag.url_hash = 'collection'
    self.contact_link.tag.url_hash = 'contact'
    self.home_link.tag.url_hash = 'home'
    self.news_link.tag.url_hash = 'news'
    self.user_link.tag.url_hash = 'user'
  
  """
  Method
  """
  
  # Set active link color
  def on_navigation(self, **nav_args):
    # this method is called whenever routing navigates to a new url
    # an example of setting the link as selected 
    # depending on the url_hash that is being navigated to
    for link in self.links:
      link.role = 'selected' if link.tag.url_hash == nav_args['url_hash'] else ''
      
  # Clean cache
  def clean_cache(self, **event_args):
    routing.set_url_hash('', replace_current_url=True)
    routing.clear_cache()
    anvil.users.logout()
    open_form('Login')
  
  # Validation prompt
  def validation(self, message, **event_args):
    return confirm(message , buttons = [('Oui', 'Y'), ('Non', 'N'), ('Annuler', 'C')])
  
  # Date Format
  def format_date(self, date, **event_args):
    return date.strftime('%d/%m/%Y à %H:%M:%S')
  
  # Integer Format
  def format_integer(self, integer, **event_args):
    return f"{integer:,}"
  
  """
  QUERY : queries called from parent
  """
  
  # 
  def to_list(self, string, **event_args):
    return str([i.strip().capitalize() for i in string.split(',')]).replace("'","''")
  
  # Get list of labels from data table tags (callable from children)
  def get_label(self, parent, column, order = True, **event_args):
    return list(set([str(row[column]).capitalize() for row in app_tables.tags.search(tables.order_by(column, ascending = order), parent = parent)]))
  
  # Get list of dates from data table contacts (callable from children)
  def get_date(self, format, order = False , **event_args):
    return list(set([row['created'].strftime(format) for row in app_tables.contacts.search(
      tables.order_by('created', ascending = order))]))
  
  # Get tags data table to list (callable from children)
  def get_tags(self, parent, **event_args):
    return list(app_tables.tags.search(parent = parent))
    
  """
  LINK : method called when a navigation link is clicked
  """
  
  # Routing navigation
  def nav_link_click(self, **event_args):
    url_hash = event_args['sender'].tag.url_hash
    routing.set_url_hash(url_hash)
    
  # Refresh
  def refresh_click(self, **event_args):
    routing.reload_page()
    
  # Logout
  def logout_link_click(self, **event_args):
    answer = self.validation('Voulez-vous vous déconnecter?')
    if answer == 'Y':
      self.clean_cache()