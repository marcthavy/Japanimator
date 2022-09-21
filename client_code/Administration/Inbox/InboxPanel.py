from ._anvil_designer import InboxPanelTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .EmailForm import EmailForm
from datetime import datetime

from HashRouting import routing

class InboxPanel(InboxPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Format current item data binding into labels.
    self.created_label.text = f"Reçu le {get_open_form().format_date(date = self.item['created'])}"
    self.category_label.text = self.item['category'].capitalize()
    
  """
  LINK : method called when the link is clicked
  """
  
  # Routing to email form with target id.
  def email_link_click(self, **event_args):
    routing.set_url_hash(
      f"email?id={self.item['id']}",
      item = self.item
    )