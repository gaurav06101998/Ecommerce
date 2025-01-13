from admin_tools.dashboard import modules, Dashboard
from django.utils.translation import gettext_lazy as _

class CustomDashboard(Dashboard):
    """
    Custom dashboard for the admin interface.
    """

    def init_with_context(self, context):
        # Welcome widget
        self.children.append(
            modules.LinkList(
                _('Quick Links'),
                children=[
                    {
                        'title': _('Home'),
                        'url': '/',
                        'external': False,
                    },
                    {
                        'title': _('Add Product'),
                        'url': 'shop/product/add/',
                        'external': False,
                    },
                    {
                        'title': _('View Orders'),
                        'url': 'shop/order/',
                        'external': False,
                    },
                ]
            )
        )

        # Sales Summary Widget
        self.children.append(
            modules.DashboardModule(
                title=_('Sales Summary'),
                children=[
                    'Total Sales This Month: $10,000',
                    'Orders Completed: 120',
                ],
                template='dashboard/widgets/sales_summary.html',
            )
        )

        # Graph Widget
        self.children.append(
            modules.DashboardModule(
                title=_('Sales Graph'),
                template='dashboard/widgets/sales_graph.html',
            )
        )

        # Static Information or Logs
        self.children.append(
            modules.DashboardModule(
                title=_('Recent Activities'),
                template='dashboard/widgets/recent_activities.html',
            )
        )
