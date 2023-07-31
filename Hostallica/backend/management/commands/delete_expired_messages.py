from django.core.management.base import BaseCommand
from backend.models import Message

class Command(BaseCommand):
    help = 'Deletes expired messages'

    def handle(self, *args, **kwargs):
        Message.delete_expired_messages()
