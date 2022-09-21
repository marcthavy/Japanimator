from ._anvil_designer import EmailFormTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('email', url_keys=['id'], title = 'Email-{id}')

class EmailForm(EmailFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Set current logged user data into variable. (called from parent)
    self.user = get_open_form().user
    
    # Toggle edition status to display unload pop-up.
    self.editing_status = False
    
  """
  METHOD
  """
  
  # Delete row of current email from contacts data table. (callback)
  def delete(self, **event_args):
    anvil.server.call(
      'delete_email',
      user = self.user,
      email = self.item
    )
    
  # Request confirmation before unload modifications.
  def before_unload(self, **event_args):
    # Show confirmation pop-up.
    if self.editing_status:
      answer = get_open_form().validation('Voulez-vous enregistrer les modifications?')
      if answer == 'C':
        # Stop unload.
        return True
      if answer == 'Y':
        self.save_button_click()
      if answer == 'N':
        # Clean up the form so clicking back shows the cached form with the old text.
        self.cancel_button_click()
        
  # Update row of current email into contacts data table. (callback)
  def update(self, **event_args):
    anvil.server.call(
      'update_email',
      user = self.user,
      email = self.item,
      category = self.category_dropdown.selected_value,
      topic = self.topic_textarea.text,
      message = self.message_textarea.text,
      status = self.status_checkbox.checked
    )
    
  # Switch modifications buttons on UI update.
  def update_ui(self, editing_status):
    self.editing_status = editing_status
    routing.set_warning_before_app_unload(editing_status)
    self.category_dropdown.enabled = self.editing_status
    self.topic_textarea.enabled = self.editing_status
    self.message_textarea.enabled = self.editing_status
    self.edit_button.visible = not self.editing_status
    self.trash_button.visible = not self.editing_status
    self.save_button.visible = self.editing_status
    self.cancel_button.visible = self.editing_status
    
  """
  SHOW : This method is called when the form is shown on the screen
  """
  
  def form_show(self , **event_args):
    # Load tag name with contact parent from tags data table into dropdown.
    self.category_dropdown.items = get_open_form().get_label(
      parent = 'contact',
      column = 'name'
    )
    self.category_dropdown.selected_value = self.item['category'].capitalize()
    
    # Try to get current email based on id when item not found. (callback)
    if not self.item:
      try:
        self.item = anvil.server.call(
          'get_email_by_id',
          user = self.user,
          i = self.url_dict['id']
        )
      except:
        # The item doesn't exist!
        routing.set_url_hash(
          'email',
          replace_current_url = True
        )
        raise Exception(f"Il semble que le mail n°{self.url_dict['id']} n'existe pas")
        
  """
  BUTTON : method called when a button link is clicked
  """
  
  # Cancel modifications.
  def cancel_button_click(self, **event_args):
    self.update_ui(editing_status = False)
    
  # Start modifications.
  def edit_button_click(self, **event_args):
    self.update_ui(editing_status = True)
    
  # Save modifications.
  def save_button_click(self, **event_args):
    self.update()
    self.update_ui(editing_status = False)
    
  # Remove current email from cache and redirect into inbox form.
  def trash_button_click(self, **event_args):
     # Show confirmation pop-up.
    answer = get_open_form().validation(
      f"Supprimer le mail n°{self.url_dict['id']} ?"
    )
    if answer == 'Y':
      self.delete()
      
      # Prevent loading current page from cache.
      routing.remove_from_cache(self.url_hash)  
      routing.set_url_hash(
        'inbox',
        replace_current_url = True
      ) 
      
      # Show notification pop-up.
      Notification(
        f"Le mail n°{self.url_dict['id']} supprimé avec succès",
        timeout = 1
      ).show()