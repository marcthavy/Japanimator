from ._anvil_designer import UserTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from plotly import graph_objects as go

from HashRouting import routing
@routing.route('users', title = 'Users management')

class User(UserTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
  """
  SHOW : This method is called when the form is shown on the screen
  """
  
  def form_show(self, column = 'last_login', **event_args):
    # Load items from users data table into repeating panel.
    self.user_panel.items = app_tables.users.search(tables.order_by(
      column,
      ascending = False
    ))
    
    # Plot bar chart based on users data table.
    self.plot_chart.data = go.Histogram(x=[row[column] for row in self.user_panel.items])
    self.plot_chart.layout.paper_bgcolor = get_open_form().bgcolor
    self.plot_chart.layout.plot_bgcolor = get_open_form().bgcolor
    
  """
  BUTTON : method called when a button link is clicked.
  """
  
  # Display users by their date of last login.
  def last_login_button_click(self, **event_args):
    self.form_show('last_login')
    
  # Display users by their date of registration.
  def sign_up_button_click(self, **event_args):
    self.form_show('signed_up')