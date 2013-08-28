# -*- coding: utf-8 -*-

import unittest

from .base import BaseComposedPermision
from .base import BasePermissionComponent
from .base import And, Or


def create_component(value, instance=False):
    class SimpleComponent(BasePermissionComponent):
        def has_permission(self, permission, request, view):
            return value

        def has_object_permission(self, permission, request, view, obj):
            return value

    if instance:
        return SimpleComponent()
    return SimpleComponent


def create_permission(callback1, callback2=None):
    class Permission(BaseComposedPermision):
        if callback1:
            global_permission_set = lambda self: callback1()

        if callback2:
            object_permission_set = lambda self: callback2()

    return Permission


class CorePermissionFrameworkTests(unittest.TestCase):

    def test_permission_with_unique_component(self):
        Component = create_component(True)
        Permission = create_permission(lambda: Component, None)

        permission = Permission()
        self.assertTrue(permission.has_permission(None, None))

        #self.assertTrue(len(permission._permission_set.components), 1)

    def test_permission_with_two_components_as_list(self):
        Component = create_component(True)
        Permission = create_permission(lambda: [Component, Component], None)

        permission = Permission()
        self.assertTrue(permission.has_permission(None, None))
        self.assertTrue(len(permission.global_permission_set()), 2)

    def test_permission_with_or_permission_set_01(self):
        Permission = create_permission(lambda: Or(
                                    create_component(True),
                                    create_component(True),
                                    create_component(True)), None)

        permission = Permission()
        self.assertTrue(permission.has_permission(None, None))
        self.assertTrue(len(permission.global_permission_set().components), 3)


    def test_permission_with_or_permission_set_02(self):
        # | operator only works for instances and not classes
        components = (lambda: Or(
                        create_component(False)(),
                        create_component(False)(),
                        create_component(True)()))

        Permission = create_permission(components, components)

        permission = Permission()
        self.assertTrue(permission.has_permission(None, None))
        self.assertTrue(permission.has_object_permission(None, None, None))
        self.assertIsInstance(permission.global_permission_set(), Or)
        self.assertTrue(len(permission.global_permission_set().components), 3)

    def test_permission_with_or_permission_set_03(self):
        # | operator only works for instances and not classes
        components = (lambda:
                        create_component(False)() |
                        create_component(False)() |
                        create_component(True)())

        Permission = create_permission(components, components)

        permission = Permission()
        self.assertTrue(permission.has_permission(None, None))
        self.assertTrue(permission.has_object_permission(None, None, None))
        self.assertTrue(len(permission.object_permission_set().components), 3)

    def test_permission_with_and_permission_set_01(self):
        Permission = create_permission(lambda: And(
                                    create_component(True),
                                    create_component(True),
                                    create_component(True)))

        permission = Permission()
        self.assertTrue(permission.has_permission(None, None))
        self.assertTrue(len(list(permission.global_permission_set().components)), 3)


    def test_permission_with_and_permission_set_02(self):
        Permission = create_permission(lambda: And(
                                    create_component(False),
                                    create_component(False),
                                    create_component(True)))

        permission = Permission()
        self.assertFalse(permission.has_permission(None, None))
        self.assertTrue(len(list(permission.global_permission_set().components)), 3)

    def test_permission_with_and_permission_set_03(self):
        Permission = create_permission(lambda: create_component(False)() &
                                               create_component(False)() &
                                               create_component(True)() )

        permission = Permission()
        self.assertFalse(permission.has_permission(None, None))
        self.assertTrue(len(permission.global_permission_set().components), 3)

    def test_permission_with_complex_compositions_01(self):
        TrueComponent = create_component(True)
        FalseComponent = create_component(False)

        permissions_set = (TrueComponent() & TrueComponent()) | FalseComponent()
        permission = create_permission(lambda: permissions_set)()

        self.assertTrue(permission.has_permission(None, None))

    def test_permission_with_complex_compositions_02(self):
        TrueComponent = create_component(True)
        FalseComponent = create_component(False)

        permissions_set = ((TrueComponent() & TrueComponent()) &
                                (FalseComponent() | (TrueComponent() & TrueComponent())))
        permission = create_permission(lambda: permissions_set)()

        self.assertTrue(permission.has_permission(None, None))

    def test_permission_with_complex_compositions_03(self):
        TrueComponent = create_component(True)
        FalseComponent = create_component(False)

        permissions_set = ((TrueComponent() & TrueComponent()) &
                                (FalseComponent() | (FalseComponent() & TrueComponent())))
        permission = create_permission(lambda: permissions_set)()

        self.assertFalse(permission.has_permission(None, None))


from .generic import components

class GenericComponentsTests(unittest.TestCase):
    def make_mock(self):
        class Mock(object):
            pass

        return Mock()

    def make_request(self):

        request = self.make_mock()
        request.user = self.make_mock()
        return request

    def test_allow_all(self):
        instance = components.AllowAll()
        self.assertTrue(instance.has_permission(None, None, None))

    def test_allow_only_anonymous(self):
        request = self.make_request()
        request.user.is_anonymous = lambda: True

        instance = components.AllowOnlyAnonymous()
        self.assertTrue(instance.has_permission(None, request, None))

    def test_allow_authenticated(self):
        request = self.make_request()
        request.user.is_anonymous = lambda: False

        instance = components.AllowOnlyAuthenticated()
        self.assertTrue(instance.has_permission(None, request, None))

    def test_allow_safe_method_only(self):
        request = self.make_request()
        request.method = "GET"

        instance = components.AllowOnlySafeHttpMethod()
        self.assertTrue(instance.has_permission(None, request, None))

    def test_obj_attr_equality(self):
        obj = self.make_mock()
        obj.x = 1
        obj.y = 1

        instance = components.ObjectAttrEqualToObjectAttr("obj.x", "obj.y")
        self.assertTrue(instance.has_object_permission(None, None, None, obj))
