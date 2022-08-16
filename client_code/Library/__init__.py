from ._anvil_designer import LibraryTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('library', title="Library | RoutingExample")

class Library(LibraryTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.

    # ???
    self.main()
    
  # Main query
  def main(self, **event_args):
    self.elements = anvil.server.call(
      'elements',
      "WHERE genres LIKE '%" + self.genres_dropdown.selected_value + "%'" +
      (" AND nsfw = false" if not self.nsfw_checkbox.checked else "")
    )
    
    # Load dropdown genres
    self.genres_dropdown.items = (anvil.server.call('genres')
                                  if not self.nsfw_checkbox.checked
                                  else anvil.server.call('genres', '')
                                 )
    
    # Load dropdown affichage
    self.affichage_dropdown.items = ([str(i) for i in range(0 ,int(self.elements) + 1, 25)][1:5]
                                     if self.elements >= 25
                                     else ['25']
                                    )
    
    # Load dropdown pagination
    self.max = int(int(self.elements) / int(self.affichage_dropdown.selected_value)) + 2
    self.pagination_dropdown.items = ([str(i) for i in range(1, self.max, 1)]
                                      if self.elements >= 25
                                      else ['1']
                                     )
                                                  
    # Load number of elements found
    self.results.text = str(self.elements) + ' résultat(s) trouvé(s)'
    
    # Load repeating panel items
    self.offset = (int(self.affichage_dropdown.selected_value)
                   * int(self.pagination_dropdown.selected_value)
                   - int(self.affichage_dropdown.selected_value)
                  )
    
    # Load repeating panel items
    self.repeating_panel.items = anvil.server.call(
      'fetch_anime_db',
      "WHERE genres LIKE '%" + self.genres_dropdown.selected_value + "%'" +
      (" AND nsfw = false" if not self.nsfw_checkbox.checked else "") +
      " ORDER BY title ASC" +
      " LIMIT " + self.affichage_dropdown.selected_value +
      " OFFSET " + str(self.offset)
    )

  # ???
  def form_show(self, **event_args):
    self.main()