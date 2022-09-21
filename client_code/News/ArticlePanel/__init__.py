from ._anvil_designer import ArticlePanelTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing

class ArticlePanel(ArticlePanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
  """
  LINK : method called when a navigation link is clicked
  """
  
  # Routing to news form with target id.
  def title_link_click(self, **event_args):
    routing.set_url_hash(
      f"news?id={self.item['id']}",
      item = self.item
    )