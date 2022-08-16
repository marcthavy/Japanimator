from ._anvil_designer import ArticleFormTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('article', url_keys=['id'], title="Article-{id} | RoutingExample")

class ArticleForm(ArticleFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    self.editing_status = False
    if not self.url_dict['id']:
      # then url_hash is article?id=  i.e. the new article button was clicked
      # so create a new article
      self.item = anvil.server.call('create_new_article')
      
      # next replace the current url
      routing.set_url_hash(f'article?id={self.item["id"]}', 
                           replace_current_url=True,
                           redirect = False
                          )
    
    elif not self.item:
      try:
        self.item = anvil.server.call('get_article_by_id',self.url_dict['id'])
      except:
        # the item doesn't exist!
        routing.set_url_hash('articles', replace_current_url=True)
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
    routing.set_url_hash('articles', replace_current_url=True) 
    Notification(f"Article {self.url_dict['id']} successfully deleted", timeout=1).show()

  def edit_button_click(self, **event_args):
    self.body_text_area.text = self.body_label.text
    self.update_ui(editing_status=True)

  def save_button_click(self, **event_args):
    # this saves the new text to the database via data binding
    self.item['body']    = self.body_text_area.text
    self.body_label.text = self.body_text_area.text
    self.update_ui(editing_status=False)
  def cancel_button_click(self, **event_args):
    self.update_ui(editing_status=False)

  def update_ui(self, editing_status):
    self.editing_status = editing_status
    routing.set_warning_before_app_unload(editing_status)
      
    self.body_label.visible = not self.editing_status
    self.body_text_area.visible = self.editing_status
    
    self.edit_button.visible = not self.editing_status
    self.trash_button.visible = not self.editing_status
    self.save_button.visible = self.editing_status
    self.cancel_button.visible = self.editing_status












