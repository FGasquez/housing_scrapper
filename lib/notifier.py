import logging
import random
import time
from lib.null_notifier import NullNotifier
from lib.discord import DiscordNotifier
from lib.sslless_session import SSLlessSession

class Notifier(NullNotifier):

    def __init__(self, config):
        self.notifiers = {}
        
        for notifier_key in config:
            notifier = config[notifier_key]
            if notifier['type'] == 'telegram':
                self.notifiers[notifier_key] = TelegramNotifier(notifier)
            elif notifier['type'] == 'discord':
                self.notifiers[notifier_key] = DiscordNotifier(notifier)
            else:
                logging.warning(f"Notifier type {notifier['type']} not supported.")

    def notify(self, properties):
        for prop in properties:
            for notifier_name in prop['notifiers']:
                if not notifier_name in self.notifiers:
                    logging.warning(f"Notifier '{notifier_name}' not found.")
                    continue
                notifier = self.notifiers.get(notifier_name)
                if notifier:
                    notifier.notify([prop])
                else:
                    logging.warning(f"Notifier '{notifier_name}' not found.")

    @staticmethod
    def get_instance(config):
        return Notifier(config)
