# from rest_framework.permissions import BasePermission


# class IsStaffOrAccOwner(BasePermission):
#     """
#     Custom permission to allow access only to staff or the account owner.
#     """

#     def has_permission(self, request, view):
#         # Allow access if the user is staff (applies to all requests)
#         return request.user and request.user.is_staff

#     def has_object_permission(self, request, view, obj):
#         # Allow access if the user is the account owner or a staff member
#         return request.user == obj or request.user.is_staff
