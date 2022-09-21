from ._anvil_designer import AnimeFormTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('anime', url_keys = ['id'], title = 'Anime-{id}')

class AnimeForm(AnimeFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    # Set current logged user data into variable. (called from parent)
    self.user = get_open_form().user
    
    # Toggle edition status to display unload pop-up.
    self.editing_status = False
    
    # Load dropdowns on admin privilege access.
    if self.user['admin']:
      for dropdown, parent in {
        self.media_dropdown:'media',
        self.status_dropdown:'status',
        self.source_dropdown:'source',
        self.season_dropdown:'season',
        self.rating_dropdown:'rate'
      }.items():
          dropdown.items = get_open_form().get_label(
            parent = parent,
            column = 'name'
      )
          
      self.weekdays_dropdown.items = [name[2:].capitalize() for name in get_open_form().get_label(
        parent = 'weekdays',
        column = 'name'
      )]
      
  """
  METHOD
  """
  
  # Request confirmation before unload modifications.
  def before_unload(self, **event_args):
    # Display confirmation pop-up.
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
  
  # Insert/Update row into japanimator.animes database. (callback)
  def upsert(self, insert = False, **event_args):
      new_id = anvil.server.call(
      'upsert_anime',
      insert = insert,
      anime_id = None if insert else self.item['id'],
      title = self.title_textbox.text, # Ne doit pas être vide !!!
      media_type = self.media_dropdown.selected_value.lower(),
      mean = "'None'" if not self.mean_textbox.text else float(self.mean_textbox.text),
      num_scoring_users = "'None'" if not self.num_scoring_users_textbox.text else int(self.num_scoring_users_textbox.text),
      status = self.status_dropdown.selected_value.lower(),
      num_episodes = "'None'" if not self.num_episodes_textbox.text else int(self.num_episodes_textbox.text),
      start_date = self.start_datepicker.date,
      end_date = self.end_datepicker.date,
      source = self.source_dropdown.selected_value.lower(),
      num_list_users = "'None'" if not self.num_list_users_textbox.text else int(self.num_list_users_textbox.text),
      popularity = "'None'" if not self.popularity_textbox.text else int(self.popularity_textbox.text),
      num_favorites = "'None'" if not self.num_favorites_textbox.text else int(self.num_favorites_textbox.text),
      rank = "'None'" if not self.rank_textbox.text else int(self.rank_textbox.text),
      average_episode_duration = self.duration_textbox.text,
      rating = self.rating_dropdown.selected_value.lower(),
      start_season_year = "'None'" if not self.season_year_textbox.text or len(str(self.season_year_textbox.text)) != 4 else self.season_year_textbox.text,
      start_season_season = self.season_dropdown.selected_value.lower(),
      broadcast_day_of_the_week = self.weekdays_dropdown.selected_value.lower(),
      broadcast_start_time = 'None' if not self.release_hour_textbox.text else self.release_hour_textbox.text,
      genres = 'None' if not self.genres_textarea.text else get_open_form().to_list(self.genres_textarea.text), # Ne doit pas être vide !!!
      studios = 'None' if not  self.studios_textarea.text else get_open_form().to_list(self.studios_textarea.text),
      synopsis = self.synopsis_textarea.text,
      nsfw = self.nsfw_checkbox.checked,
      main_picture_medium = self.main_picture_medium_textbox.text,
      main_picture_large = self.main_picture_large_textbox.text,
      alternative_titles_en = self.alternative_titles_en_textbox.text,
      alternative_titles_ja = self.alternative_titles_jp_textbox.text,
      alternative_titles_synonyms = 'None' if not self.alternative_titles_synonyms_textbox.text else get_open_form().to_list(self.alternative_titles_synonyms_textbox.text) #null
      )
      
      # Redirect to anime form on insert with returning id. (callback)
      if insert:
        self.editing_status = False
        self.item = anvil.server.call(
          'fetch_anime_db',
          ' WHERE id = ' + str(new_id)
        )[0]
        set_url_hash(
          f'anime?id={str(new_id)}'
        )
  
  # Delete row of current anime from japanimator.animes database. (callback)
  def delete(self, **event_args):
    anvil.server.call(
      'delete_anime',
      id = self.item['id']
    )
    
  # Switch modifications buttons on UI update.
  def update_ui(self, editing_status = False, new = False, **event_args):
    self.editing_status = editing_status
    routing.set_warning_before_app_unload(editing_status)
    
    # Display.
    for component in [
      self.title_textbox,
      self.mean_textbox,
      self.rank_textbox,
      self.popularity_textbox,
      self.num_scoring_users_textbox,
      self.num_list_users_textbox,
      self.num_favorites_textbox,
      self.edit_urls_panel,
      self.edit_informations_panel,
      self.synopsis_textarea,
      self.genres_textarea,
      self.studios_textarea,
      self.edit_alternative_titles_panel
    ]:
      component.visible = self.editing_status
      
    # Hide.
    for component in [
      self.edit_button,
      self.trash_button,
      self.title_label,
      self.informations_panel,
      self.synopsis_label,
      self.alternative_titles_panel,
    ]:
      component.visible = not self.editing_status
    
    # Toggle buttons between add and edit.
    if new:
      self.add_button.visible = self.editing_status
    else:
      self.save_button.visible = self.editing_status
      self.cancel_button.visible = self.editing_status
    
  """
  SHOW : This method is called when the form is shown on the screen
  """
  
  def form_show(self, **event_args):
    # Create new anime when id is not found.
    if not self.url_dict['id']:
      self.recommandation_title.visible = self.editing_status
      self.update_ui(
        new = True,
        editing_status = True
      )
      
      # Initialize dropdowns selected value.
      for obj in [
        self.media_dropdown,
        self.status_dropdown,
        self.source_dropdown,
        self.season_dropdown,
        self.weekdays_dropdown,
        self.rating_dropdown
      ]:
        obj.selected_value = 'Nc'
      
    # Try to fetch current new anime if routing failed. (callback)
    else:
      if not self.item:
        try:
          self.item = anvil.server.call(
            'fetch_anime_db',
            ' WHERE id = ' + self.url_dict['id']
          )[0]
        except:
          # The item doesn't exist!
          routing.load_error_form()
          raise Exception(f"Il semble que l'anime n°{self.url_dict['id']} n'existe pas")
      # Load dropdowns data bindings on admin privilege access.
      if self.user['admin']:
        self.edit_button.visible = not self.editing_status
        self.trash_button.visible = not self.editing_status
        
        for dropdown, column in {
            self.media_dropdown:'media_type',
            self.status_dropdown:'status',
            self.source_dropdown:'source',
            self.season_dropdown:'start_season_season',
            self.weekdays_dropdown:'broadcast_day_of_the_week',
            self.rating_dropdown:'rating'
        }.items():
          dropdown.selected_value = self.item[column].replace('_', ' ').capitalize()
          
        for textbox, column in {
          self.genres_textarea:'genres',
          self.studios_textarea:'studios',
          self.alternative_titles_synonyms_textbox:'alternative_titles_synonyms'
        }.items():
          textbox.text = None if not self.item[column] else ', '.join(eval(self.item[column]))
        
      else:
        self.edit_button.visible = self.editing_status
        self.trash_button.visible = self.editing_status
        self.add_button.visible = self.editing_status
        
      # Format current item data binding into labels to avoid none error.
      self.mean_label.text = 'NC' if not self.item['mean'] else str("{:.2f}".format(float(self.item['mean']))).replace('.', ',')
      self.rank_label.text = 'NC' if not self.item['rank'] else get_open_form().format_integer(self.item['rank'])
      self.popularity_label.text = 'NC' if not self.item['popularity'] else get_open_form().format_integer(self.item['popularity'])
      self.num_scoring_users_label.text = 'NC' if not self.item['num_scoring_users'] else get_open_form().format_integer(self.item['num_scoring_users'])
      self.num_list_users_label.text = 'NC' if not self.item['num_list_users'] else get_open_form().format_integer(self.item['num_list_users'])
      self.num_favorites_label.text = 'NC' if not self.item['num_favorites'] else get_open_form().format_integer(self.item['num_favorites'])
      
      self.media_label.text = self.item['media_type'].capitalize()
      self.num_episodes_label.text = 'Nc' if not self.item['num_episodes'] else self.item['num_episodes']
      self.duration_label.text = 'Nc' if not self.item['average_episode_duration'] else self.item['average_episode_duration'][7:]
      self.status_label.text = self.item['status'].replace('_', ' ').capitalize()
      self.source_label.text = self.item['source'].replace('_', ' ').capitalize()
      self.season_label.text = 'Nc' if not self.item['start_season_year'] else f"{self.item['start_season_season'].capitalize()} {self.item['start_season_year']}"
      self.broadcast_dates_label.text = 'Nc' if not self.item['start_date'] or not self.item['end_date'] else f"{self.item['start_date'][:10]} au {self.item['end_date'][:10]}"
      self.release_weekday_label.text = 'Nc' if not self.item['broadcast_start_time'] else f"{self.item['broadcast_day_of_the_week'].capitalize()} at {self.item['broadcast_start_time']}"
      self.rating_label.text = self.item['rating'].replace('_', ' ').capitalize()
      
      self.genre_panel.items = None if not self.item['genres'] else eval(self.item['genres'])
      self.studio_panel.items = None if not self.item['studios'] else eval(self.item['studios'])
      self.alternative = list(filter(None, set([self.item['alternative_titles_en'], self.item['alternative_titles_ja']])))
      self.alternative_titles_panel.items = self.alternative.remove(self.item['title']) if self.item['title'] in self.alternative else self.alternative
      
      # Load recommandations based on current anime into repeating panel. (callback)
      self.recommandation_panel.items = anvil.server.call(
        'recommandation',
        self.item['id']
      )
    
  """
  BUTTON : method called when a button link is clicked
  """
  
  # Cancel modifications.
  def cancel_button_click(self, **event_args):
    self.update_ui(insert = False)
    
  # Start modifications.
  def edit_button_click(self, **event_args):
    self.update_ui(editing_status = True)
    
  # Save modifications.
  def save_button_click(self, **event_args):
    self.upsert()
    self.update_ui()

  def add_button_click(self, **event_args):
    self.upsert(insert = True)

  # Remove current email from cache and redirect into inbox form.
  def trash_button_click(self, **event_args):
     # Display confirmation pop-up.
    answer = get_open_form().validation(
      f"Supprimer l'anime n°{self.url_dict['id']} ?"
    )
    if answer == 'Y':
      self.delete()
      #don't want to load current page from cache.
      routing.remove_from_cache(self.url_hash)  
      routing.set_url_hash(
        'collection',
        replace_current_url = True
      ) 
      
      # Display notification pop-up.
      Notification(
        f"L'anime n°{self.url_dict['id']} supprimé avec succès",
        timeout = 1
      ).show()