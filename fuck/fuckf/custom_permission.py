from rest_framework import permissions

#Permission Level
# Admin (Same as Owner or Not, it's up to you.)
#   - Read, write, 
# Owner : (tmporary we call it as is_staff flag sets True)
#   - Read, write, 
# User : 
#   - Read, write
# Guest 
#   - Read


class IsOwner(permissions.BasePermission): # read that Private Cateogry, or Post is not allowed.
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.is_staff:
            return True
        else :
            return False

class IsOwnerOrConditionalReadOnly(permissions.BasePermission): # read that Private Cateogry, or Post is not allowed.
    """
    A base class from which all permission classes should inherit.
    """
    # def has_permission(self, request, view):
    #     """
    #     Return `True` if permission is granted, `False` otherwise.
    #     """
    #     return False
    def has_object_permission(self, request, view, obj):
        # 읽기 권한 요청이 들어오면 허용
        print("ser")
        if request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS and obj.is_private == False:
            return True
        else:
            return False