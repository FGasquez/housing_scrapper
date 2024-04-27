#!/usr/bin/env python

import logging
import yaml
from lib.notifier import Notifier
from providers.processor import process_properties

# logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# configuration    
with open("configuration.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

disable_ssl = False
if 'disable_ssl' in cfg:
    disable_ssl = cfg['disable_ssl']

logging.debug(cfg)

notifier = Notifier.get_instance(cfg['notifiers'])

new_properties = []
for provider_name, provider_data in cfg['providers'].items():
    try:
        logging.info(f"Processing provider {provider_name}")
        new_properties += process_properties(provider_name, provider_data)
        logging.info('Prcessed')
    except Exception as e:
        logging.error(traceback.format_exc())
        logging.error(f"Error processing provider {provider_name}.\n{str(e)}")

logging.info(f"Properties found: {len(new_properties)}")

if len(new_properties) > 0:
    notifier.notify(new_properties)
