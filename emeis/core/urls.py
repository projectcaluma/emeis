from rest_framework.routers import SimpleRouter

from . import views

r = SimpleRouter(trailing_slash=False)

r.register(r"users", views.UserViewSet)
r.register(r"scopes", views.ScopeViewSet)
r.register(r"roles", views.RoleViewSet)
r.register(r"permissions", views.PermissionViewSet)
r.register(r"acls", views.ACLViewSet)

urlpatterns = r.urls
