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
@routing.route('contact', title='Contact | RoutingExample')

class Contact(ContactTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Load items on dropdown
    self.category_dropdown.items = get_open_form().get_label('category')
    
    # Initiate input
    self.clear_input()
    
  # Input initialisation
  def clear_input(self):
    self.category_dropdown.placeholder
    self.subject_textbox.text = ''
    self.message_textarea.text = ''
    
  """
  BUTTON
  """
  
  # Send
  def send_button_click(self, **event_args):
    # Check required field list(set([str(row['category']) for row in app_tables.labels.search()]))[:-1]
    if (not self.category_dropdown.selected_value in self.category_dropdown.items
        or not self.subject_textbox.text
        or not self.message_textarea.text
       ):
      alert('Veuillez remplir les champs obligatoires')
    else:
      
      # Insert input into data table
      user = anvil.server.call('get_user')
      anvil.server.call('add_row', user['email'],
                        self.category_dropdown.selected_value,
                        self.subject_textbox.text,
                        self.message_textarea.text)
      
      # Send notification
      self.notification = get_open_form().get_label('notification')
      for index in range(len(self.category_dropdown.items)):
        if self.category_dropdown.selected_value == self.category_dropdown.items[index]:
          Notification(self.notification[index], timeout = 0).show()

      # Re-initiate input
      self.clear_input()