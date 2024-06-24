import telegram
import time
import logging
from lib.null_notifier import NullNotifier

class TelegramNotifier(NullNotifier):
    def __init__(self, config):
        self.config = config

        if config['enabled'] is False:
            return NullNotifier()

        self.bot = telegram.Bot(token=self.config['token'])
        self.chat_id = self.config['chat_id']

        if self.config.get('disable_ssl', False):
            self.bot = telegram.Bot(token=self.config['token'], request=SSLlessSession())
        else:
            self.bot = telegram.Bot(token=self.config['token'])

    def notify(self, properties):
        logging.debug(f'Notifying to Telegram about {len(properties)} properties')
        
        if len(self.config['messages']) > 0:
            text = random.choice(self.config['messages'])
            self.bot.send_message(chat_id=self.chat_id, text=text)
        
        for prop in properties:
            logging.debug(f"Notifying about {prop['url']}")
            self.bot.send_message(chat_id=self.chat_id,
                                  text=f"[{prop['title']}]({prop['url']})",
                                  parse_mode=telegram.ParseMode.MARKDOWN)
            # delay between messages
            time.sleep(self.config.get('delay', 0))
