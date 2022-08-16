from ._anvil_designer import ListArticlesFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('articles', title="Article | RoutingExample")

class ListArticlesForm(ListArticlesFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    self.repeating_panel_1.items = anvil.server.call('get_articles')
    
  def new_article_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    routing.set_url_hash('article?id=', load_from_cache=False)
    routing.remove_from_cache('article?id=') 
    # just in case we also don't want this form to load from cache from back/forward navigation
    
  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    self.repeating_panel_1.items = anvil.server.call_s('get_articles')