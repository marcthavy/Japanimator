from ._anvil_designer import UserTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('user', title='User | RoutingExample')

class User(UserTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    self.init()

  def init(self, **event_args):
    # Loading current user avatar
    self.user = anvil.server.call('get_user')
    self.default = 'https://www.adenine-rh.com/wp-content/themes/consultix/images/no-image-found-360x250.png'
    if self.user['avatar']:
      self.avatar.source = self.user['avatar'].url
    else:
      self.avatar.source = self.default
    
    # Loading user profil
    self.email.text = "Email : " + self.user['email']
    self.registered.text = "Membre depuis le : " + str(self.user['signed_up'])[0:10]
    self.visited.text = "Dernière connexion le : " + str(self.user['last_login'])[0:10]
  
  # Image loader
  def file_loader_change(self, file, **event_args):
    
    # Upsert new avatar
    self.user.update(avatar = self.file_loader.file)
    
    # Reloading
    self.init()

  #Delete button
  def delete_button_click(self, **event_args):
    self.user.delete()
    open_form('Login')