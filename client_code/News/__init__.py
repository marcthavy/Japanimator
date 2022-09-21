from ._anvil_designer import NewsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('news', title='Actuality')

class News(NewsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Set the current logged user data into variable. (called from parent)
    self.user = get_open_form().user
    
    # Show privilege admin access.
    if self.user['admin']:
      self.new_article_button.visible = True
    else:
      self.new_article_button.visible = False
      
  """
  SHOW : This method is called when the column panel is shown on the screen
  """
  
  def form_show(self, **event_args):
    # Load items from news data table into repeating panel.
    self.news_panel.items = app_tables.news.search()
    
  """
  BUTTON : method called when a button link is clicked.
  """
  
  # Routing to new article form.
  def new_article_button_click(self, **event_args):
    routing.set_url_hash(
      'article?id=',
      load_from_cache = False
    )
    # Just in case we also don't want this form to load from cache from back/forward navigation.
    routing.remove_from_cache('article?id=') 