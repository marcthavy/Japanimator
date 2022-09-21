from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing

class ItemTemplate2(ItemTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def title_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    routing.set_url_hash(url_pattern='blog-post', 
                         url_dict   ={'id':self.item['id']},
                         item = self.item
                        )
    

