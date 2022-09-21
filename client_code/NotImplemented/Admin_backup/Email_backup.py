from ._anvil_designer import Email_backupTemplate
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

class Email_backup(Email_backupTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
    self.created_label.text = f"Reçu le {self.item['created'].strftime('%d/%m/%Y à %H:%M:%S')}"
    self.category_dropdown.items = get_open_form().get_label('category')
    
    self.editing_status = False
    
    if not self.item:
      try:
        self.item = anvil.server.call('get_email_by_id',self.url_dict['id'])
      except:
        # the item doesn't exist!
        routing.set_url_hash('email', replace_current_url=True)
        raise Exception(f"Il semble que le mail n°{self.url_dict['id']} n'existe pas")

  def before_unload(self):
    if self.editing_status:
      answer = confirm('Voulez-vous enregistrer les modifications?',
                  buttons=[('Oui', 'Y'), ('Non', 'N'), ('Annuler', 'C')])
      if answer == 'C':
        # stop unload
        return True
      if answer == 'Y':
        self.save_button_click()
      if answer == 'N':
        # clean up the form so clicking back shows the cached form with the old text
        self.cancel_button_click()

  def trash_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item.delete()
    routing.remove_from_cache(self.url_hash)  #don't want to load current page from cache
    routing.set_url_hash('admin', replace_current_url=True) 
    Notification(f"Le mail n°{self.url_dict['id']} supprimé avec succès", timeout=1).show()

  def edit_button_click(self, **event_args):
    self.update_ui(editing_status=True)

  def save_button_click(self, **event_args):
    # this saves the new text to the database via data binding
    self.item['created'] = self.created_datepicker.date
    self.created_label.text = f"Reçu le {self.created_datepicker.date.strftime('%d/%m/%Y à %H:%M:%S')}"
    
    self.item['category'] = self.category_dropdown.selected_value
    self.category_label.text = self.category_dropdown.selected_value
    
    self.item['subject'] = self.subject_textarea.text
    self.subject_label.text = self.subject_textarea.text
    
    self.item['message'] = self.message_textarea.text
    self.message_label.text = self.message_textarea.text
    
    self.update_ui(editing_status=False)

  def cancel_button_click(self, **event_args):
    self.update_ui(editing_status=False)

  def update_ui(self, editing_status):
    self.editing_status = editing_status
    routing.set_warning_before_app_unload(editing_status)

    self.created_card.visible = not self.editing_status
    self.created_datepicker.visible = self.editing_status
    
    self.category_card.visible = not self.editing_status
    self.category_dropdown.visible = self.editing_status
    
    self.subject_card.visible = not self.editing_status
    self.subject_textarea.visible = self.editing_status
    
    self.message_card.visible = not self.editing_status
    self.message_textarea.visible = self.editing_status
    
    self.edit_button.visible = not self.editing_status
    self.trash_button.visible = not self.editing_status
    
    self.save_button.visible = self.editing_status
    self.cancel_button.visible = self.editing_status