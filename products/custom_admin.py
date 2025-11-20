from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = "My Shop Admin"
    site_title = "My Shop Admin Portal"
    index_title = "Dashboard"

custom_admin_site = CustomAdminSite(name='custom_admin')
