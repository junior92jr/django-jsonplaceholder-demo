from typing import Dict


class ObjectDiffMixin(object):
    """Mixin model that implements difference between objects."""

    def get_difference(self, object_one: Dict, object_two: Dict) -> Dict:
        """Method that compares two dictionaries and find differences."""

        difference = [
            (key, (value, object_two[key])) for (
                key, value) in object_one.items() if value != object_two[key]
        ]

        return dict(difference)
