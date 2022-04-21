class CustomPermissionView:
    permission_classes = []
    permission_classes_by_action = {}

    def get_permissions(self):
        try:
            # return permission_classes depending on `method`
            return [permission() for permission in self.permission_classes_by_action[self.request.method]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
