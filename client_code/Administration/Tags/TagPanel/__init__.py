from ._anvil_designer import TagPanelTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class TagPanel(TagPanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Set current logged user data into variable. (called from parent)
    self.user = get_open_form().user
    
    # Load tag name with tag parent from tags data table into dropdown.
    self.parent_dropdown.items = get_open_form().get_label(
      parent = 'tag',
      column = 'name'
    )
    self.parent_dropdown.selected_value = self.item['parent'].capitalize()
    
    # Format current item data binding into labels.
    self.tag_label.text = self.item['name'].capitalize()
    
    # Protect important features by preventing deletion.
    if self.item['description'] == 'Ne pas supprimer':
      self.delete_link.visible = False
      
  """
  METHOD
  """
    
  # Delete row of current tag from tags data table. (callback)
  def delete(self, **event_args):
    anvil.server.call(
      'delete_tag',
      user = self.user,
      tag = self.item
    )
    
  # Set event listener to trigger update on parent. (event)
  def event(self, **event_args):
    self.parent.raise_event('x-refresh')
    
  # Update row of current tag into tags data table. (callback)
  def update(self, **event_args):
    anvil.server.call(
      'update_tag',
      user = self.user,
      tag = self.item,
      parent = self.parent_dropdown.selected_value,
      description = self.description_textbox.text,
      color = self.color_textbox.text
    )
    
  """
  CHANGE : method called when the dropdown value is changed.
  """
  
  # Update current tag.
  def parent_dropdown_change(self, **event_args):
    self.textbox_pressed_enter()
    self.event()
    
  """
  ENTER : method called when Enter key is trigged.
  """
  
  # Check compliance of required fields.
  def textbox_pressed_enter(self, **event_args):
    p,n,c = False, False, False
    if self.parent_dropdown.selected_value == self.item['name']:
      self.parent_dropdown.border = get_open_form().error
    else:
      self.parent_dropdown.border = None
      p = True
    if len(self.description_textbox.text.strip()) == 0:
      self.description_textbox.border = get_open_form().error
    else:
      self.description_textbox.border = None
      n = True
    if len(self.color_textbox.text.strip()) == 0:
      self.color_textbox.border = get_open_form().error
    else:
      self.color_textbox.border = None
      c = True
    if p and n and c:
      self.update()
      
  """
  LINK : method called when a navigation link is clicked
  """
  
  # Delete current tag.
  def delete_link_click(self, **event_args):
    # Show confirmation pop-up.
    answer = get_open_form().validation(
      f"Supprimer le tag '{self.item['name']}' ?"
    )
    if answer == 'Y':
      self.delete()
      self.event()