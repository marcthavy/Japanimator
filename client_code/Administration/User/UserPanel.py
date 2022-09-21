from ._anvil_designer import UserPanelTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class UserPanel(UserPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Set current logged user data into variable. (called from parent)
    self.user = get_open_form().user
    
  """
  METHOD
  """
  
  # Update row of current tag into tags data table. (callback)
  def update(self, **event_args):
    anvil.server.call(
      'update_user',
      user = self.user,
      row = self.item,
      confirmed = self.confirmed_checkbox.checked,
      enabled = self.enabled_checkbox.checked,
      admin = self.admin_checkbox.checked
    )