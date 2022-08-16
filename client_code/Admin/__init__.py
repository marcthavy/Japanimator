from ._anvil_designer import AdminTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from HashRouting import routing
@routing.route('admin', title="admin | RoutingExample")

class Admin(AdminTemplate):
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
    self.refresh_all(refresh = True)
    
  # Cards refresher
  def refresh_all(self,refresh = False, **event_args):
    self.unreaded.text = len(app_tables.contacts.search(status = False))
    self.readed.text = len(app_tables.contacts.search(status = True))
    self.all.text = len(app_tables.contacts.search())
    if refresh:
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
      status = (True
                if self.status_dropdown.selected_value in self.status_dropdown.items[-1]
                else False
               )
    )
      
  # just in case we also don't want this form to load from cache from back/forward navigation  
  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    """self.emails_panel.items = anvil.server.call_s('get_emails')"""
    self.refresh_all(refresh = True)