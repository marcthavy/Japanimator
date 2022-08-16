from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Login(LoginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.

  """
  BUTTON
  """
  
  # Login
  def login_button_click(self, **event_args):
    # Google authentication
    if anvil.users.login_with_form():
      open_form('Main')