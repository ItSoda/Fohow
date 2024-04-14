import asyncio

from django.core.management.base import BaseCommand

from tgbot.handlers import start_bot


class Command(BaseCommand):
    help = "Starts the Telegram bot"

    def handle(self, *args, **options):
        asyncio.run(start_bot())