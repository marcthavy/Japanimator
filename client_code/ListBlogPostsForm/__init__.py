from ._anvil_designer import ListBlogPostsFormTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('blog-posts', title="BlogPosts | RoutingExample")

class ListBlogPostsForm(ListBlogPostsFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
    self.repeating_panel_1.items = anvil.server.call('get_blog_posts')