from ._anvil_designer import ContactTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('contact', title = 'Contact us')

class Contact(ContactTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Set current logged user data into variable. (called from parent)
    self.user = get_open_form().user
    
  """
  METHOD
  """
  
  # Add new row into contacts data table. (callback)
  def create(self, **event_args):
    anvil.server.call(
      'create_email',
      user = self.user,
      category = self.category_dropdown.selected_value,
      topic = self.topic_textbox.text,
      message = self.message_textarea.text
    )
    
  """
  SHOW : This method is called when the column panel is shown on the screen
  """
  
  def form_show(self, **event_args):
    # Load tag name with contact parent from tags data table into dropdown.
    self.category_dropdown.items = get_open_form().get_label(
      parent = 'contact',
      column = 'name'
    )
    
    # Initialize contact form input.
    self.topic_textbox.text = None
    self.message_textarea.text = None
    self.topic_textbox.border = None
    self.message_textarea.border = None

  """
  BUTTON : method called when a button link is clicked.
  """
  
  # Send contact form as email.
  def send_button_click(self, **event_args):
    # Check compliance of required fields.
    if (not self.category_dropdown.selected_value in self.category_dropdown.items
        or len(self.topic_textbox.text.strip()) == 0
        or len(self.message_textarea.text.strip()) == 0
       ):
      alert('Veuillez remplir les champs obligatoires')
    else:
      self.create()
      
      # Show notification pop-up.
      Notification(app_tables.tags.get(
        parent = 'contact',
        name = self.category_dropdown.selected_value.lower())['description'],
        timeout = 0
      ).show()
      
      # Re-initialize contact form input.
      self.form_show()
      
  """
  CHANGE : method called when the text is written into textbox/textarea.
  """
  
  # Show visual indication of required message field status
  def message_textarea_change(self, **event_args):
    if len(self.message_textarea.text.strip()) > 0 :
      self.message_textarea.border = None
    else:
      self.message_textarea.border = get_open_form().error
      
  # Show visual indication of required topic field status
  def topic_textbox_change(self, **event_args):
    if len(self.topic_textbox.text.strip()) > 0 :
      self.topic_textbox.border = None
    else:
      self.topic_textbox.border = get_open_form().error