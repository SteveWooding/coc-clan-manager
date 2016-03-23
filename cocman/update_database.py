"""Update the database with the given clan tag."""

from sqlalchemy.orm.exc import NoResultFound

from coc.api import ClashOfClans

from cocman import app
from cocman.database_setup import Clan, Member
from cocman.connect_to_database import connect_to_database



def update_database(clan_tag):
    # Connect to the database
    session = connect_to_database()

    # Get the clan data from the API
    coc_api = ClashOfClans(app.config['COC_API_KEY'])
    clan_data = coc_api.clans(clan_tag).get()

    # Create or update clan details
    try:
        # Get clan object to be updated
        clan = session.query(Clan).filter_by(tag=clan_tag).one()
        clan.name = clan_data['name']
    except NoResultFound:
        # Create a new clan object
        clan = Clan(
            name=clan_data['name'],
            tag=clan_data['tag']
        )

    # Update optional data items
    clan.badge_url_medium = clan_data['badgeUrls']['medium']
    clan.badge_url_small = clan_data['badgeUrls']['small']

    # Commit the clan object to the database
    session.add(clan)
    session.commit()

    


