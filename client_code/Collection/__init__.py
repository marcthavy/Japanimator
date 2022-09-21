from ._anvil_designer import CollectionTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('collection', title = 'Anime Collection')

class Collection(CollectionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Initialize suggestion panel with empty value.
    self.suggestion_panel.items = [{'text': ' '}] * 3
    
    # Set event listener on children (n-1) when a title is selected from suggestion panel.
    self.suggestion_panel.set_event_handler(
      'x-option_clicked',
      self.option_clicked
    )
    
  """
  SHOW : This method is called when the form is shown on the screen
  """
  
  def form_show(self, search = True, **event_args):
    # Load all titles from japanimator.animes database into variable. (callback)
    self.options = anvil.server.call(
      'column',
      column = 'title'
    )
    
    # Load number of elements based on filters from japanimator.animes database into label. (callback)
    self.elements = anvil.server.call(
      'elements',
      (" WHERE LOWER(title) LIKE '%" + self.search_textbox.text.lower().replace("'", "''") + "%'"
       if self.search_textbox.text.strip() != ''
       else " WHERE LOWER(genres) LIKE '%" + self.genre_dropdown.selected_value.lower() + "%'") + 
      (' AND nsfw = false' if not self.nsfw_checkbox.checked else '')
    )
    self.result_label.text = str(self.elements) + ' résultat(s) trouvé(s)'
    
    # Load distinct genres from japanimator.animes database into dropdown. (callback)
    self.genre_dropdown.items = (anvil.server.call('column', column = 'genres')
                                 if not self.nsfw_checkbox.checked
                                 else anvil.server.call('genres', '')
                                )
    
    # Load number of elements to display per page into dropdown.
    self.display_dropdown.items = ([str(i) for i in range(25 ,int(self.elements) + 25, 25)][:4]
                                     if self.elements >= 25
                                     else ['25']
                                    )
    
    # Load number of pages into dropdown. (pagination)
    self.page = int(int(self.elements) / int(self.display_dropdown.selected_value))
    self.max = int(self.page) if int(int(self.elements) % int(self.display_dropdown.selected_value)) == 0 else int(self.page) + 1
    self.pagination_dropdown.items = ([str(i) for i in range(1, self.max + 1, 1)]
                                      if self.elements >= 25
                                      else ['1']
                                     )
    
    # Load limit & offset to dispplay into repeating panel.
    self.offset = (int(self.display_dropdown.selected_value)
                   * int(self.pagination_dropdown.selected_value)
                   - int(self.display_dropdown.selected_value)
                  )
    
    # Hide links on form show.
    for link in [
      self.next_head_link,
      self.previous_head_link,
      self.next_foot_link,
      self.previous_foot_link
    ]:
      link.visible = False
    
    # Display links based on pagination.
    if int(self.pagination_dropdown.selected_value) < self.max:
      self.next_head_link.visible = self.next_foot_link.visible = True
    if int(self.pagination_dropdown.selected_value) <= self.max and int(self.pagination_dropdown.selected_value) != 1:
      self.previous_head_link.visible = self.previous_foot_link.visible = True
    
    # Load items based on filters from japanimator.animes database into repeating panel.
    self.anime_panel.items = anvil.server.call(
      'fetch_anime_db',
      (" WHERE LOWER(title) LIKE '%" + self.search_textbox.text.lower().replace("'", "''") + "%'"
       if self.search_textbox.text.strip() != '' else
       " WHERE LOWER(genres) LIKE '%" + self.genre_dropdown.selected_value.lower() + "%'") +
      (' AND nsfw = false' if not self.nsfw_checkbox.checked else '') +
      ' ORDER BY title ASC' +
      ' LIMIT ' + self.display_dropdown.selected_value +
      ' OFFSET ' + str(self.offset)
    )
    
  """
  BUTTON : method called when a button link is clicked
  """
  
  # Routing to new article form.
  def new_anime_button_click(self, **event_args):
    routing.set_url_hash(
      'anime?id=',
      load_from_cache = False
    )
    # Just in case we also don't want this form to load from cache from back/forward navigation.
    routing.remove_from_cache('anime?id=') 
  
  # Reset all filters.
  def reset_button_click(self, **event_args):
    self.search_textbox.text = None
    self.genre_dropdown.enabled = True
    self.suggestion_panel.items = [{'text': ' '}] * 3
    self.form_show()
    
  """
  LINK : method called when the link is clicked
  """
  
  # Display next result.
  def next_link_click(self, **event_args):
    self.pagination_dropdown.selected_value = str(int(self.pagination_dropdown.selected_value) + 1)
    self.form_show()
  
  # Filter per title selected from suggestion.
  def option_clicked(self, option, **event_args):
    if option == ' ':
      return
    self.search_textbox.text = option
    self.suggestion_panel.items = [{'text': ' '}] * 3
    self.form_show()
  
  # Display previous result.
  def previous_link_click(self, **event_args):
    self.pagination_dropdown.selected_value = str(int(self.pagination_dropdown.selected_value) - 1)
    self.form_show()
    
  """
  CHANGE : method called when the text is written into textbox/textarea.
  """
  
  # Filter per genre.
  def genre_dropdown_change(self, **event_args):
    self.search_textbox.text = None
    self.form_show()
  
  # Load suggestions based on search into repeating panel.
  def search_textbox_change(self, **event_args):
      self.genre_dropdown.enabled = False
      new_options = []
      for option in self.options:
        # if option.lower().startswith(self.search_textbox.text.lower()):
        if self.search_textbox.text.lower() in option.lower():
          new_options.append({'text':option})
      # Truncate to 3 max
      new_options = new_options[:3]
      # Ensure a full 3 options
      if len(new_options) < 3:
        new_options+=([{'text':' '}] * (3 - len(new_options)))
      self.suggestion_panel.items = new_options
      
  """
  ENTER : method called when Enter key is trigged.
  """
  
  # Filter per title.
  def search_textbox_pressed_enter(self, **event_args):
    self.suggestion_panel.items = [{'text': ' '}] * 3
    self.form_show()