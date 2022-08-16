from ._anvil_designer import BlogPostFormTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('blog-post', url_keys = ['id'], title="BlogPost-{id} | RoutingExample")

class BlogPostForm(BlogPostFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    if not self.item:
      try:
        self.item = anvil.server.call('get_blog_post_by_id', self.url_dict['id'])
      except:
        routing.load_error_form()
        raise Exception(f'no blogpost with id {self.url_dict["id"]}')