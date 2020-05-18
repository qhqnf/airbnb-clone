from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "It tells me love you"

    def add_arguments(self, parser):
        parser.add_argument(
            "--times", help="How many times do you want me to tell that I love you",
        )

    def handle(self, *args, **options):
        times = options.get("times")
        for i in range(int(times)):
            print("I love you")
