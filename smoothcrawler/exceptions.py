
class GlobalizeObjectError(Exception):

    def __str__(self):
        return "Cannot globalize target object because it is None object."

