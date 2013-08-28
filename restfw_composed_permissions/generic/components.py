# -*- coding: utf-8 -*-

from rest_framework import permissions
from ..base import (BasePermissionComponent,
                    BaseComposedPermision,
                    And, Or)


class AllowAll(BasePermissionComponent):
    """
    Always allow all requests without
    any constraints.
    """

    def has_permission(self, permission, request, view):
        return True


class AllowOnlyAnonymous(BasePermissionComponent):
    """
    Allow only anonymous requests.
    """

    def has_permission(self, permission, request, view):
        return request.user.is_anonymous()


class AllowOnlyAuthenticated(BasePermissionComponent):
    def has_permission(self, permission, request, view):
        if request.user.is_anonymous():
            return False
        return True


class AllowOnlySafeHttpMethod(BasePermissionComponent):
    def has_permission(self, permission, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class ObjectAttrEqualToObjectAttr(BasePermissionComponent):
    """
    This is a object level permision component and if is used on
    global permission context it always returns True.

    This component checks the equality of two expressions that are
    evaluted in "safe" way. On the context of eval are exposed "obj"
    as current object and "request" as the current request.

    This component works well for check a object owner os similary.

    Example:

    .. code-block:: python

        class SomePermission(BaseComposedPermision):
            global_permission_set = (lambda self: AllowAll)
            object_permission_set = (lambda self:
                                        ObjectAttrEqualToObjectAttr("request.user", "obj.owner"))
    """

    def __init__(self, obj_attr1, obj_attr2):
        self.obj_attr1 = obj_attr1
        self.obj_attr2 = obj_attr2

    def has_object_permission(self, permission, request, view, obj):
        safe_locals = {"obj": obj, "request": request}

        try:
            attr1_value = eval(self.obj_attr1, {}, safe_locals)
            attr2_value = eval(self.obj_attr2, {}, safe_locals)
        except AttributeError:
            return False
        else:
            return attr1_value == attr2_value
