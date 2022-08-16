from ._anvil_designer import EmailTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing

@routing.route('email', url_keys=['id'], title="Email-{id} | RoutingExample")
class Email(EmailTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.editing_status = False
    if not self.item:
      try:
        self.item = anvil.server.call('get_email_by_id',self.url_dict['id'])
      except:
        # the item doesn't exist!
        routing.set_url_hash('email', replace_current_url=True)
        raise Exception(f"It looks like Article {self.url_dict['id']} doesn't exist")
        
  def before_unload(self):
    if self.editing_status:
      r = confirm('Do you want to save the changes?',
                  buttons=[('Yes', 'Y'), ('No', 'N'), ('Cancel', 'C')])
      if r == 'C':
        # stop unload
        return True
      if r == 'Y':
        self.save_button_click()
      if r == 'N':
        # clean up the form so clicking back shows the cached form with the old text
        self.cancel_button_click()

  def trash_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item.delete()
    routing.remove_from_cache(self.url_hash)  #don't want to load current page from cache
    routing.set_url_hash('admin', replace_current_url=True) 
    Notification(f"email {self.url_dict['id']} successfully deleted", timeout=1).show()

  def edit_button_click(self, **event_args):
    self.message_text_area.text = self.message_label.text
    self.update_ui(editing_status=True)

  def save_button_click(self, **event_args):
    # this saves the new text to the database via data binding
    self.item['message'] = self.message_text_area.text
    self.message_label.text = self.message_text_area.text
    self.update_ui(editing_status=False)

  def cancel_button_click(self, **event_args):
    self.update_ui(editing_status=False)

  def update_ui(self, editing_status):
    self.editing_status = editing_status
    routing.set_warning_before_app_unload(editing_status)
      
    self.message_label.visible = not self.editing_status
    self.message_text_area.visible = self.editing_status

    self.category_label.visible = not self.editing_status
    self.category_dropdown.visible = self.editing_status
    
    self.edit_button.visible = not self.editing_status
    self.trash_button.visible = not self.editing_status
    self.save_button.visible = self.editing_status
    self.cancel_button.visible = self.editing_status