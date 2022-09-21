from ._anvil_designer import Admin_backupTemplate
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

from HashRouting import routing
@routing.route('admin', title="admin | RoutingExample")

class Admin_backup(Admin_backupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    """self.emails_panel.items = anvil.server.call('get_emails')"""
    # Any code you write here will run when the form opens.
  
    # Load items on dropdowns
    self.year_dropdown.items = get_open_form().get_date('%Y', 'year')
    self.month_dropdown.items = get_open_form().get_date('%B', 'month_order')
    self.category_dropdown.items = get_open_form().get_label('category')
    self.status_dropdown.items = get_open_form().get_label('status')
    
    # Initiate cards & repeating panel
    self.refresh_all()
    
  # Cards refresher
  def refresh_all(self, status = False, **event_args):
    
    self.email_label.text = 'Répartition des mails ' + self.status_dropdown.selected_value.lower() + 's'
    """self.status_value = True if self.status_dropdown.selected_value in self.status_dropdown.items[-1] else False"""
    self.status_value = status
    
    self.unreaded.text = len(app_tables.contacts.search(status = False))
    self.readed.text = len(app_tables.contacts.search(status = True))
    self.all.text = len(app_tables.contacts.search())
    
    self.unreaded_link.text = len(app_tables.contacts.search(status = False))
    self.readed_link.text = len(app_tables.contacts.search(status = True))
    
    labels = list(set([row['category'] for row in app_tables.contacts.search(status=self.status_value)]))
    values = [len(app_tables.contacts.search(category = i, status=self.status_value)) for i in labels]
    colors = ['black', 'lightcyan','cyan','royalblue','darkblue','lightcyan'] #  set colors for slices
    
    self.plot_pie.data = go.Pie(labels=labels,
                                values=values,
                                hole=0.5,
                                showlegend=False,
                                textinfo='label',
                                sort=False,
                                rotation=90,
                                marker = dict(colors= colors),
                               )
    self.plot_pie.layout.margin = dict(t=0, b=0, l=0, r=0)
    self.plot_pie.config = dict(displayModeBar = False)
    self.plot_pie.layout.font.size = "9.5"
    
    self.refresh_repeating_panel()

  # Repeating panel refresher
  def refresh_repeating_panel(self, **event_args):
    self.emails_panel.items = app_tables.contacts.search(
      tables.order_by('created', ascending = False),
      year = (int(self.year_dropdown.selected_value)
              if self.year_dropdown.selected_value in self.year_dropdown.items
              else q.not_(0)
             ),
      month = (self.month_dropdown.selected_value
               if self.month_dropdown.selected_value in self.month_dropdown.items
               else q.not_('Mois')
              ),
      category = (self.category_dropdown.selected_value
               if self.category_dropdown.selected_value in self.category_dropdown.items
               else q.not_('category')
              ),
      status = (self.status_value)
    )
      
  # just in case we also don't want this form to load from cache from back/forward navigation  
  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    """self.emails_panel.items = anvil.server.call_s('get_emails')"""
    self.refresh_all()
    
  def readed_link_click(self, **event_args):
    self.refresh_all(True)