from rest_framework import permissions
from .permissions import IsAccOwnerOrAdmin


class IsStaffPermissionMixin:
    permission_classes = [permissions.IsAdminUser, IsAccOwnerOrAdmin]
