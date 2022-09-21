from ._anvil_designer import UserFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('user', title = 'User profile')

class UserForm(UserFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Set current logged user data into variable. (called from parent)
    self.item = get_open_form().user
    
  """
  METHOD
  """
  
  # Delete row of current user from users data table.
  def delete(self, **event_args):
    anvil.server.call(
      'delete_account',
      user = self.item
    )
    
  # Set avatar on current user row into users data table.
  def insert(self, **event_args):
    anvil.server.call(
      'set_avatar',
      user = self.item,
      img = self.avatar_loader.file
    )
    
  # Set new password on current user row into users data table.
  def update(self, **event_args):
    anvil.server.call(
      'set_password',
      user = self.item,
      new_password = self.confirm_new_password_textbox.text
    )
    
  """
  SHOW : This method is called when the form is shown on the screen
  """
  
  def form_show(self, **event_args):
    # Format current item data binding into labels.
    self.registered_label.text = f"{get_open_form().format_date(self.item['signed_up'])}"
    self.visited_label.text = f"{get_open_form().format_date(self.item['last_login'])}"
    self.account_label.text = 'Administrateur' if self.item['admin'] else 'Membre'
    
  """
  BUTTON : method called when a button link is clicked.
  """
  
  # Delete account of current user.
  def delete_button_click(self, **event_args):
    # Show confirmation pop-up.
    answer = get_open_form().validation(
      'Voulez-vous supprimer votre compte définitivement?'
    )
    if answer == 'Y':
      self.delete()
      
      # Clean local cache.
      get_open_form().clean_cache()
      
  """
  CHANGE : method called when file is loaded.
  """
  
  # Display avatar of current user.
  def avatar_loader_change(self, file, **event_args):
    self.avatar_image.source = self.avatar_loader.file
    self.insert()
    
  """
  ENTER : method called when Enter key is trigged.
  """
  
  # Check new password compliance.
  def new_password_textbox_pressed_enter(self, **event_args):
    if (len(self.new_password_textbox.text.strip()) < 6 or
        len(self.new_password_textbox.text.strip()) > 50
       ):
      self.new_password_textbox.border = get_open_form().error
      self.invalid_lenght_label.visible = True
    else:
      self.new_password_textbox.enabled = False
      self.new_password_textbox.border = get_open_form().valid
      self.invalid_lenght_label.visible = False
      self.confirm_new_password_textbox.enabled = True
      self.confirm_new_password_textbox.focus()
      
  # Re-check new password compliance.
  def confirm_new_password_textbox_pressed_enter(self, **event_args):
    if self.confirm_new_password_textbox.text != self.new_password_textbox.text:
      self.confirm_new_password_textbox.border = get_open_form().error
      self.invalid_password_label.visible = True
    else:
      self.confirm_new_password_textbox.enabled = False
      self.confirm_new_password_textbox.border = get_open_form().valid
      self.invalid_password_label.visible = False
      self.valid_password_label.visible = True
      self.update()