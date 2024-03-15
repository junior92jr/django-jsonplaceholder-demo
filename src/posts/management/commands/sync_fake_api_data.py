from django.core.management.base import BaseCommand, CommandError

from posts.tasks import sync_posts, sync_comments


class Command(BaseCommand):
    """class that create a django admin command."""

    help = "Syncronize Posts and Comments from an external API."

    def handle(self, *args, **options) -> None:
        """Method that handles the command."""

        try:
            sync_posts.syncronize_posts_task()

            self.stdout.write(
                self.style.SUCCESS("'Post(s)' sycronized."))

            sync_comments.syncronize_comments_task()

            self.stdout.write(
                self.style.SUCCESS("'Comment(s)' sycronized."))

        except Exception as error:
            raise CommandError(
                f"Command stopped for an unexpected error: {error}")
