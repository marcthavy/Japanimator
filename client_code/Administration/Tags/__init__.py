from ._anvil_designer import TagsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('tag', title = 'Tag management')

class Tags(TagsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Set current logged user data into variable. (called from parent)
    self.user = get_open_form().user
    
    # Set event listener on children (n-1) to trigger updating repeating panel.
    self.parent_panel.set_event_handler(
      'x-refresh',
      self.form_show
    )
    
  """
  METHOD
  """
  
  # Add new row into tags data table. (callback)
  def create(self, **event_arg):
    anvil.server.call(
      'create_tag',
      user = self.user,
      name = self.new_tag_textbox.text
    )
    
  """
  SHOW : This method is called when the form is shown on the screen
  """
  
  def form_show(self, **event_arg):
    # Load items from tags data table into repeating panel.
    self.parent_panel.items = get_open_form().get_tags(
      parent = 'tag'
    )
    
  """
  ENTER : method called when Enter key is trigged.
  """
  
  # Check compliance of required field.
  def new_tag_textbox_pressed_enter(self, **event_args):
    if len(self.new_tag_textbox.text.strip()) == 0:
      self.new_tag_textbox.border = get_open_form().error
    else:
      self.create()
      self.form_show()
      self.new_tag_textbox.text = None
      self.new_tag_textbox.border = None