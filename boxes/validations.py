class BoxUpsertValidations:
    @classmethod
    def validate_create_box(cls, user):
        if user.is_staff:
            return True
        else:
            return False

    @classmethod
    def validate_update_box_request(cls, user):
        return cls.validate_create_box(user=user)

    @classmethod
    def validate_my_box_list_request(cls, user):
        return cls.validate_create_box(user=user)

    @classmethod
    def validate_delete_box(cls, user,box):
        if box.created_by == user.username:
            return True
        return False