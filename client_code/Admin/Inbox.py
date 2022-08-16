from ._anvil_designer import InboxTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .Email import Email
from datetime import datetime

from HashRouting import routing

class Inbox(InboxTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    #
    self.created_label.text = f"le {self.item['created'].strftime('%d/%m/%Y à %H:%M:%S')}"

  def title_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    # alternative way to navigate to a form
    routing.set_url_hash(f"email?id={self.item['id']}", item=self.item)