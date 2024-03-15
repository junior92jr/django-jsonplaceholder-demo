import logging

from typing import List, Dict

from django.db import DatabaseError


logger = logging.getLogger(__name__)


class ObjectImporter(object):
    """Method that implements Objects logic for create and update."""

    def __init__(self, model_class: object,
                 external_objects: List[Dict],
                 validator_class: object,
                 bulk_create: object,
                 bulk_update: object) -> None:
        """Constructor that init Import generic classes."""

        self._objects_to_bulk = external_objects
        self._model_class = model_class
        self.validator_class = validator_class
        self._bulk_create = bulk_create
        self._bulk_update = bulk_update

    def _validate_objects(self) -> bool:
        return self.validator_class(
            data=self._objects_to_bulk, many=True).is_valid()

    def _collect_to_create(self) -> None:
        """Method that collects objects not present in the database."""

        self._objects_to_create = []
        objects_to_insert_ids = [
            obj['id'] for obj in self._objects_to_bulk]

        self._objects_to_create = [
            obj for obj in self._objects_to_bulk if not obj[
                'id'] in list(self._model_class.objects.filter(
                    external_id__in=objects_to_insert_ids).values_list(
                        'external_id', flat=True))
        ]

    def _collect_to_update(self) -> None:
        """Method that collects objects to update from the database."""

        self._objects_to_update = []
        _objects_to_update_ids = [
            obj['id'] for obj in self._objects_to_bulk]

        self._objects_to_update = [
            obj for obj in self._objects_to_bulk if obj[
                'id'] in list(self._model_class.objects.filter(
                    external_id__in=_objects_to_update_ids).values_list(
                        'external_id', flat=True))
        ]

    def _insert_data_in_chunks(self) -> None:
        """Method that bulk insert chunks of objects."""

        for obj in self._objects_to_create:
            try:
                if self._process_insert(obj):
                    self._bulk_create.add(self._model_class(**obj))
            except DatabaseError as error:
                logger.error(f'Error ocurred during bulk insert: {error}')
                continue
        self._bulk_create.done()

    def _update_data_in_chunks(self) -> None:
        """Method that bulk update chunks of objects."""

        for obj in self._objects_to_update:
            try:
                if self._process_update(obj):
                    self._bulk_update.add(self._model_class(**obj))
            except DatabaseError as error:
                logger.error(f'Error ocurred during bulk update: {error}')
                continue
        self._bulk_update.done()

    def synchronize_data(self) -> None:
        """Method that sync object data into the database."""

        if not self._validate_objects():
            raise ValueError('Payload structure is not valid.')

        self._collect_to_create()
        self._collect_to_update()
        self._insert_data_in_chunks()
        self._update_data_in_chunks()

    def _process_insert(self, obj: Dict) -> Dict:
        """Method must be implemented in child class."""

        raise NotImplementedError()

    def _process_update(self, obj: Dict) -> Dict:
        """Method must be implemented in child class."""

        raise NotImplementedError()
