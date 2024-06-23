import logging
from providers.mercadolibre import MercadoLibre
from providers.pads import Pads
from providers.zonaprop import Zonaprop
from providers.inmobusqueda import Inmobusqueda
from providers.properati import Properati
from sqlalchemy.orm import sessionmaker
from lib.database import Database

def register_property(session, prop):
    try:
        new_property = Database.Property(
            internal_id=prop['internal_id'],
            provider=prop['provider'],
            url=prop['url']
        )
        session.add(new_property)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)

def process_properties(provider_name, provider_data):
    provider = get_instance(provider_name, provider_data)

    new_properties = []

    # Initialize the Database object
    db = Database()
    session = db.create_session()

    try:
        for prop in provider.next_prop():
            logging.debug(f"Processing property {prop}")
            # Check to see if we know it
            existing_property = session.query(Database.Property).filter_by(
                internal_id=prop['internal_id'],
                provider=prop['provider']
            ).first()

            if existing_property is None:
                # Insert and save for notification
                logging.debug('It is a new one')
                register_property(session, prop)
                new_properties.append(prop)
    except Exception as e:
        session.rollback()
        print(e)
    finally:
        session.close()

    return new_properties


def get_instance(provider_name, provider_data):
    if provider_name == 'pads':
        return Pads(provider_name, provider_data)
    elif provider_name == 'mercadolibre':
        return MercadoLibre(provider_name, provider_data)
    elif provider_name == 'zonaprop':
        return Zonaprop(provider_name, provider_data)
    elif provider_name == 'inmobusqueda':
        return Inmobusqueda(provider_name, provider_data)
    elif provider_name == 'properati':
        return Properati(provider_name, provider_data)
    else:
        raise Exception('Unrecognized provider')