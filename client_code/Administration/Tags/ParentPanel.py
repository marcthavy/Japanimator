from ._anvil_designer import ParentPanelTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ParentPanel(ParentPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Load items from tags data table into repeating panel.
    self.tag_panel.items = get_open_form().get_tags(
      parent = self.item['name']
    )
    self.parent_label.text = self.item['name'].capitalize()
    
    # Set event listener on children (n-2).
    self.tag_panel.set_event_handler(
      'x-refresh',
      self.bounce
    )
    
  """
  METHOD
  """
  
  # Carry event child (n-2) to parent (n).
  def bounce(self, **event_arg):
    self.parent.raise_event('x-refresh')