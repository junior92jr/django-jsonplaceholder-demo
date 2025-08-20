from django.core.management.base import BaseCommand, CommandError

from content.utils.synchronizers import (
    synchronize_comments_task,
    synchronize_posts_task,
)


class Command(BaseCommand):
    """
    Django command to synchronize Posts and Comments from an external API.
    """

    help = "Synchronize Posts and Comments from an external API."

    def handle(self, *args, **options) -> None:
        """
        Main entry point for the command.
        """

        try:
            synchronize_posts_task()
            self.stdout.write(self.style.SUCCESS("Posts synchronized successfully."))

            synchronize_comments_task()
            self.stdout.write(self.style.SUCCESS("Comments synchronized successfully."))

        except Exception as error:
            raise CommandError(f"Command stopped due to an unexpected error: {error}")
