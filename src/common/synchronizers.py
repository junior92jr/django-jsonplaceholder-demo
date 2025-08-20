import logging
from typing import Any, Dict, List, Type

from django.db import models, transaction

logger = logging.getLogger(__name__)


class BaseSyncService:
    """
    Base class for synchronizing external API data into a Django model.
    Subclasses must define model, handler, and implement map_fields.
    """

    model: Type[models.Model] = None
    handler_class = None
    unique_field: str = "external_id"

    def map_fields(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert API item dict into model field mapping.
        Must be implemented by subclasses.
        """
        raise NotImplementedError

    def synchronize(self) -> None:
        """
        Run the synchronization: fetch API data and bulk sync into DB.
        """
        handler = self.handler_class()

        try:
            data = handler.list_items()
            logger.info(f"{len(data)} '{self.model.__name__}(s)' fetched from API.")
        except Exception as error:
            logger.error(f"Failed to fetch {self.model.__name__}s from API: {error}")
            raise

        inserted_count, updated_count = self._bulk_sync(data)

        logger.info(f"{inserted_count} '{self.model.__name__}(s)' inserted.")
        logger.info(f"{updated_count} '{self.model.__name__}(s)' updated.")

    def _bulk_sync(self, api_data: List[Dict[str, Any]]) -> tuple[int, int]:
        """
        Shared bulk sync implementation using dict comparison.
        """
        with transaction.atomic():
            new_objects, objects_to_update, inserted_count, updated_count = (
                self._prepare_sync_lists(api_data)
            )
            self._bulk_insert(new_objects)
            self._bulk_update(objects_to_update)
        return inserted_count, updated_count

    def _prepare_sync_lists(self, api_data: List[Dict[str, Any]]):
        """
        Compare API data with existing objects and separate into
        new objects vs objects that need update.
        """
        existing_objects = self.model.objects.in_bulk(field_name=self.unique_field)
        new_objects = []
        objects_to_update = []
        inserted_count = 0
        updated_count = 0

        for item in api_data:
            external_id = item.get("id")
            if external_id is None:
                continue

            fields = self.map_fields(item)

            if external_id in existing_objects:
                obj = existing_objects[external_id]
                obj_dict = obj.as_field_dict(include=fields.keys())
                if obj_dict != fields:
                    for k, v in fields.items():
                        setattr(obj, k, v)
                    objects_to_update.append(obj)
                    updated_count += 1
            else:
                new_objects.append(
                    self.model(**{self.unique_field: external_id, **fields})
                )
                inserted_count += 1

        return new_objects, objects_to_update, inserted_count, updated_count

    def _bulk_insert(self, new_objects):
        """
        Perform bulk create if there are new objects.
        """
        if new_objects:
            self.model.objects.bulk_create(new_objects, ignore_conflicts=True)

    def _bulk_update(self, objects_to_update):
        """
        Perform bulk update if there are updated objects.
        """
        if objects_to_update:
            fields = list(objects_to_update[0].as_field_dict().keys())
            self.model.objects.bulk_update(objects_to_update, fields)
