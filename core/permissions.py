from rest_framework import permissions

<<<<<<< HEAD
class isAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.isAdmin 
=======
class isTruck(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.name == 'truck' 

class isCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role.name == 'customer'
>>>>>>> 778f979f7a12139edbef23bb48924bdad3f294c1
