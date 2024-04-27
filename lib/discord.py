import time
from lib.null_notifier import NullNotifier
from discord import SyncWebhook

class DiscordNotifier(NullNotifier):
    def __init__(self, config):
        self.config = config
        if config['enabled'] is False:
            return NullNotifier()

        self.webhook = SyncWebhook.from_url(config['webhook_url'])
        self.messages = config.get('messages', [])
    
    def notify(self, properties):
        logging.info(f'Notifying to Discord about {len(properties)} properties')
        
        if len(self.messages) > 0:
            text = random.choice(self.messages)
            self.webhook.send(content=text, username='Property Notifier')

        for prop in properties:
            logging.debug(f"Notifying about {prop['url']}")
            self.webhook.send(content=f"[{prop['title']}]({prop['url']})", username='Property Notifier')
            time.sleep(self.config.get('delay', 0))