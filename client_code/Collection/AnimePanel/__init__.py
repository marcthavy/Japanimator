from ._anvil_designer import AnimePanelTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing

class AnimePanel(AnimePanelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Format current item data binding into labels to avoid none error.
    self.score_label.text = 'NC' if self.item['mean'] == None else str("{:.2f}".format(float(self.item['mean']))).replace('.', ',')
    self.rank_label.text = 'NC' if self.item['rank'] == None else get_open_form().format_integer(self.item['rank'])
    self.genre_label.text = 'NC' if not self.item['genres'] else ', '.join(eval(self.item['genres']))
    self.season_label.text = 'NC' if self.item['start_season_year'] == self.item['start_season_season'] else f"{self.item['start_season_season'].capitalize()} {self.item['start_season_year']}"
    self.synopsis_label.text = 'NC' if self.item['synopsis'] == None else (self.item['synopsis'][:400] + '...')
    
  # Routing to anime form with target id.
  def title_link_click(self, **event_args):
    routing.set_url_hash(url_pattern = 'anime', 
                         url_dict = {'id':self.item['id']},
                         item = self.item
                        )