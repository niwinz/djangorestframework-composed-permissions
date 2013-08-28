# -*- coding: utf-8 -*-

from .generics import *


class AllowAnyPermission(BaseComposedPermision):
    global_permission_set = (lambda self: AllowAll)
    object_permission_set = (lambda self: AllowAll)
