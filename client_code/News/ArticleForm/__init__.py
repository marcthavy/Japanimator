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
@routing.route('news', url_keys=['id'], title='news-{id}')

class ArticleForm(ArticleFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Set the current logged user data into variable. (called from parent)
    self.user = get_open_form().user
    
    # Show privilege admin access.
    if self.user['admin']:
      self.edit_button.visible = True
      self.trash_button.visible = True
    else:
      self.edit_button.visible = False
      self.trash_button.visible = False
      
    # Toggle edition status.
    self.editing_status = False
    
  """
  SHOW : This method is called when the column panel is shown on the screen
  """
  
  def form_show(self, **event_args):
    # Create new article when id is not found.
    if not self.url_dict['id']:
      self.item = anvil.server.call('create_new_article')
      
      # Replace the current routing url
      routing.set_url_hash(f"news?id={self.item['id']}", 
                           replace_current_url = True,
                           redirect = False
                          )
    # Try to fetch current new article if routing failed
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
    self.item.delete()
    #don't want to load current page from cache
    routing.remove_from_cache(self.url_hash)  
    routing.set_url_hash('news', replace_current_url=True) 
    Notification(f"Article {self.url_dict['id']} successfully deleted", timeout=1).show()

  def edit_button_click(self, **event_args):
    self.body_text_area.text = self.body_label.text
    self.update_ui(editing_status=True)

  def save_button_click(self, **event_args):
    # this saves the new text to the database via data binding
    self.item['body']  = self.body_text_area.text
    self.body_label.text = self.body_text_area.text
    self.update_ui(editing_status=False)
  def cancel_button_click(self, **event_args):
    self.update_ui(editing_status=False)

  def update_ui(self, editing_status):
    self.editing_status = editing_status
    self.poster_loader.visible = self.editing_status
    
    routing.set_warning_before_app_unload(editing_status)
      
    self.body_label.visible = not self.editing_status
    self.body_text_area.visible = self.editing_status
    
    self.edit_button.visible = not self.editing_status
    self.trash_button.visible = not self.editing_status
    self.save_button.visible = self.editing_status
    self.cancel_button.visible = self.editing_status

  # Insert/Update current user avatar
  def poster_loader_change(self, file, **event_args):
    self.item['image'] = self.poster_loader.file
    self.poster_image.source = self.poster_loader.file