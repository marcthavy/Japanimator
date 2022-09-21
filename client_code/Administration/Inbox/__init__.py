from ._anvil_designer import InboxTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import plotly.graph_objects as go
from ... import Globals

from HashRouting import routing
@routing.route('inbox', title = 'Inbox mail')

class Inbox(InboxTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    
  """
  METHOD
  """
  
  # Load items based on filters from contacts data table into repeating panel.
  def refresh_repeating_panel(self, order = False, **event_args):
    self.inbox_panel.items = app_tables.contacts.search(
      tables.order_by(
        'created',
        ascending = order
      ),
      year = (int(self.year_dropdown.selected_value)
              if self.year_dropdown.selected_value in self.year_dropdown.items
              else q.not_(0)
             ),
      category = (self.category_dropdown.selected_value.lower()
               if self.category_dropdown.selected_value in self.category_dropdown.items
               else q.not_('category')
              ),
      status = self.status
    )
    
  """
  SHOW : This method is called when the form is shown on the screen
  """
  
  def form_show(self, **event_args):
    # Load distinct years from contacts data table into dropdown.
    self.year_dropdown.items = list(set([row['created'].strftime('%Y') for row in app_tables.contacts.search(
      tables.order_by(
        'created',
        ascending = False
      ))]))
    
    # Load distinct categories from contacts data table into dropdown.
    self.category_dropdown.items = list(set([row['category'].capitalize() for row in app_tables.contacts.search(tables.order_by(
      'category',
      ascending = True
    ),status = Globals.toggle)]))
    
    # Load number of emails from contacts data table into labels.
    self.unreaded_link.text = len(app_tables.contacts.search(status = False))
    self.readed_link.text = len(app_tables.contacts.search(status = True))
    self.all_label.text = int(self.unreaded_link.text) + int(self.readed_link.text)
    
    # Set labels, values and colors list into variables.
    self.labels = self.category_dropdown.items
    self.values = [len(app_tables.contacts.search(category = label.lower(),status =  Globals.toggle)) for label in self.labels]
    self.colors = [app_tables.tags.get(name = label.lower())['color'] for label in self.labels]
    
    # Plot pie based on contacts data table split per categories.
    self.plot_pie.data = go.Pie(
      labels = self.labels,
      values = self.values,
      hole = 0.5,
      showlegend = False,
      textinfo = 'label',
      sort = False,
      rotation = 90,
      marker = dict(colors = self.colors)
    )
    
    self.plot_pie.layout.margin = dict(t=0, b=0, l=0, r=0)
    self.plot_pie.config = dict(displayModeBar = False)
    self.plot_pie.layout.font.size = '9.5'
    self.plot_pie.layout.paper_bgcolor = get_open_form().bgcolor
    
    # Toggle between readed and unreaded email.
    self.status = Globals.toggle
    
    # Display emails filtered & sorted.
    self.refresh_repeating_panel()
    
  """
  CHANGE : method called when the dropdown value is changed.
  """
  
  # Display sorted emails by date of receipt.
  def tri_dropdown_change(self, **event_args):
    if self.order_dropdown.selected_value == 'Les plus récents':
      self.refresh_repeating_panel(order = False)
    else:
      self.refresh_repeating_panel(order = True)
      
  """
  LINK : method called when a navigation link is clicked
  """
  
  # Display emails by readed status.
  def readed_link_click(self, **event_args):
    Globals.toggle = True
    self.form_show()
    
  # Display emails by unreaded status.
  def unreaded_link_click(self, **event_args):
    Globals.toggle = False
    self.form_show()