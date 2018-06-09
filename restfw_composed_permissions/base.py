# -*- coding: utf-8 -*-

import copy
import inspect


from rest_framework import permissions


class BaseComposedPermission(permissions.BasePermission):
    """
    Base class for compose permission with permission
    components and logical operators.

    This class should have permission_set defined as
    a instance function or lambda.

    Examles:

    .. code-block:: python

        class SomePermission(BaseComposedPermision):
            global_permission_set = (lambda self: Component1() | Component2())
            object_permission_set = (lambda self: Component1() | Component2())

    .. code-block:: python

        class SomePermission(BaseComposedPermision):
            def global_permission_set(self):
                return (Component1() | Component2())

            def object_permission_set(self):
                return (Component1() | Component2())

    Defining a permission set as function instead of
    a class attribute directly prevent storing state
    on the component instances.

    `permission_set` method or lambda function should
    return a iterable, `BasePermissionComponent` or
    `BasePermissionSet` subclass instance.

    Example:

    .. code-block: python

        class SomePermission(BaseComposedPermision):
            global_permission_set = (lambda self: [Component1, Component2])
            # Is same as:
            # global_permission_set = (lambda self: Component1() | Component2())
    """

    def global_permission_set(self):
        raise NotImplementedError()

    def object_permission_set(self):
        raise NotImplementedError()

    def _evaluate_permission_set(self, permission_set):
        # Evaluate components
        permission_set = permission_set()

        if isinstance(permission_set, (list, tuple, set)):
            _permission_set = Or(*permission_set)
        elif inspect.isclass(permission_set):
            _permission_set = Or(permission_set())
        else:
            _permission_set = Or(permission_set)

        return _permission_set

    def has_permission(self, request, view):
        permission_set = self._evaluate_permission_set(self.global_permission_set)
        return permission_set.has_permission(self, request, view)

    def has_object_permission(self, request, view, obj):
        permission_set = self._evaluate_permission_set(self.object_permission_set)
        return permission_set.has_object_permission(self, request, view, obj)


class BasePermissionComponent(object):
    """
    Base class for permission component.
    Is a unit permission class.
    """

    def has_permission(self, permission, request, view):
        raise NotImplementedError()

    def has_object_permission(self, permission, request, view, obj):
        # By default return same as that "has_permission" method
        return self.has_permission(permission, request, view)

    def __and__(self, component):
        return And(self, component)

    def __or__(self, component):
        return Or(self, component)

    def __invert__(self):
        return Not(self)


class RestPermissionComponent(BasePermissionComponent):

    def _has_permission(self, permission, request, view):
        return self.has_permission(request, view)

    def _has_object_permission(self, permission, request, view, obj):
        return self.has_object_permission(request, view, obj)

    def has_permission(self, request, view):
        raise NotImplementedError()

    def has_object_permission(self, request, view, obj):
        # By default return same as that "has_permission" method
        return self.has_permission(request, view)


class BasePermissionSet(object):
    """
    Base class for permission set.
    Permission Set is composed of Permission Components
    """

    def __init__(self, *args):
        self.components = [c() if inspect.isclass(c) else c for c in args]

    def update_method_name(self, name, component):
        if isinstance(component, RestPermissionComponent):
            name = '_' + name

        return name

    def get_component_result(self, component, method_name, *args, **kwargs):
        final_method_name = self.update_method_name(method_name, component)
        method = getattr(component, final_method_name)
        return method(*args, **kwargs)

    def _check_permission(self, method_name, *args, **kwargs):
        raise NotImplementedError()

    def has_permission(self, permission, request, view):
        return self._check_permission("has_permission", permission,
                                      request, view)

    def has_object_permission(self, permission, request, view, obj):
        return self._check_permission("has_object_permission", permission,
                                      request, view, obj)
    def __invert__(self):
        return Not(self)


class Not(BasePermissionSet):
    def has_permission(self, *args, **kwargs):
        result = self.get_component_result(self.components[0], 'has_permission', *args, **kwargs)
        return not result

    def has_object_permission(self, *args, **kwargs):
        result = self.get_component_result(self.components[0], 'has_object_permission', *args, **kwargs)
        return not result


class Or(BasePermissionSet):
    def _check_permission(self, method_name, *args, **kwargs):
        valid = False

        for component in self.components:
            result = self.get_component_result(component, method_name, *args, **kwargs)
            if result:
                valid = True
                break

        return valid

    def __and__(self, component):
        return And(self, component)

    def __or__(self, component):
        components = copy.copy(self.components)
        components.append(component)
        return Or(*components)


class And(BasePermissionSet):
    def _check_permission(self, method_name, *args, **kwargs):
        valid = True

        for component in self.components:
            result = self.get_component_result(component, method_name, *args, **kwargs)
            if not result:
                valid = False
                break

        return valid

    def __and__(self, component):
        components = copy.copy(self.components)
        components.append(component)
        return And(*components)

    def __or__(self, component):
        return Or(self, component)

#Alias to old typo for backwards compatability
BaseComposedPermision = BaseComposedPermission
