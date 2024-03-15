import logging

from typing import List

from django.db import DatabaseError


logger = logging.getLogger(__name__)


class BulkTransactionManager(object):
    """Class that implements  Bulk strategies for Create and Update."""

    def __init__(self, model_class: object,
                 chunk_size: int = 100,
                 fields_lookup: List[str] = []) -> None:
        """Constructor with default values for Bulk Transactions."""

        self._model_class = model_class
        self.chunk_size = chunk_size
        self._fields_lookup = fields_lookup
        self._bulk_transaction_list = []
        self.total_inserted = 0
        self.total_updated = 0

    def add(self, obj: object) -> None:
        """Method that add an Object to the Bulk List Parameter."""

        self._bulk_transaction_list.append(obj)
        if len(self._bulk_transaction_list) >= self.chunk_size:
            self._commit()

    def done(self) -> None:
        """Method that insert the partial bulk list parameter."""

        if len(self._bulk_transaction_list) > 0:
            self._commit()

    def _commit(self) -> None:
        """Method must be implemented by the child classes."""

        raise NotImplementedError()


class BulkCreateManager(BulkTransactionManager):
    """Class that implements Bulk Create."""

    def _commit(self) -> None:
        """Perform Bulk insert transaction to the database."""

        try:
            self._model_class.objects.bulk_create(self._bulk_transaction_list)
            self.total_inserted += len(self._bulk_transaction_list)
        except DatabaseError as error:
            logger.error(f'Error in commit: {error}')
            raise error

        self._bulk_transaction_list = []


class BulkUpdateManager(BulkTransactionManager):
    """Class that implements  Bulk  Update."""

    def _commit(self) -> None:
        """Perform Bulk update transaction to the database."""

        try:
            self._model_class.objects.bulk_update(
                self._bulk_transaction_list, self._fields_lookup)
            self.total_updated += len(self._bulk_transaction_list)
        except DatabaseError as error:
            logger.error(f'Error in commit: {error}')
            raise error

        self._bulk_transaction_list = []
