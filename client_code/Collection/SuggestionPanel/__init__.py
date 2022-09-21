from ._anvil_designer import SuggestionPanelTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class SuggestionPanel(SuggestionPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
  
  # Set event listener to select current title item on parent. (event)
  def title_link_click(self, **event_args):
    self.parent.raise_event(
      'x-option_clicked',
      option = self.title_link.text
    )