from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('home', title = 'Home')  # Multiple decorators allowed
@routing.route('', title = 'Home')

class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
  """
  SHOW : This method is called when the form is shown on the screen
  """
  
  def form_show(self, **event_args):
    # Load items from news data table into repeating panel.
    self.news_panel.items = app_tables.news.search()
    
    # Load animes's release of current day from japanimator.animes database into repeating panel. (callback)
    self.release_panel.items = anvil.server.call(
    'fetch_anime_db',
    " WHERE status = 'currently_airing'" +
    " AND LOWER(broadcast_day_of_the_week) = TRIM(LOWER(to_char(CURRENT_DATE, 'Day')))"
    )
    
    # Load trends animes from japanimator.animes database into repeating panel. (callback)
    self.trends_panel.items = anvil.server.call(
    'fetch_anime_db',
    ' WHERE nsfw = false' +
    " AND start_season_year = date_part('year', CURRENT_DATE)" +
    ' AND start_season_season =' +
    " (case WHEN DATE_PART('month', CURRENT_DATE) IN (12, 1, 2) THEN 'winter'" +
          "WHEN DATE_PART('month', CURRENT_DATE) IN (3, 4, 5) THEN 'spring'" +
          "WHEN DATE_PART('month', CURRENT_DATE) IN (6, 7, 8) THEN 'summer'" +
          "WHEN DATE_PART('month', CURRENT_DATE) IN (9, 10, 11) THEN 'fall'" +
    ' END)' +
    ' AND popularity IS NOT NULL' +
    ' ORDER BY popularity ASC' +
    ' LIMIT 10'
    )
    
    # Load airing animes from japanimator.animes database into repeating panel. (callback)
    self.airing_panel.items = anvil.server.call(
      'fetch_anime_db',
      ' WHERE nsfw = false' +
      " AND status = 'currently_airing'" +
      ' ORDER BY start_date DESC' +
      ' LIMIT 10'
    )
    
    # Load recently added animes from japanimator.animes database into repeating panel. (callback)
    self.added_panel.items = anvil.server.call(
      'fetch_anime_db',
      ' WHERE nsfw = false' +
      ' AND created_at IS NOT NULL' +
      ' ORDER BY created_at DESC' +
      ' LIMIT 10'
    )
    
    # Load top animes from japanimator.animes database into repeating panel. (callback)
    self.top_panel.items = anvil.server.call(
      'fetch_anime_db',
      ' WHERE nsfw = false' +
      ' AND rank IS NOT NULL' +
      ' ORDER BY rank ASC' +
      ' LIMIT 10'
    )