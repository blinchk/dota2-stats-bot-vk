import logging
import requests
from sys import stdout

logger = logging.getLogger(__name__)
#out_hdlr = logging.StreamHandler(stdout)
#out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
#out_hdlr.setLevel(logging.INFO)
#logger.addHandler(out_hdlr)
#logger.setLevel(logging.INFO)

HEROES = None


def _load_heroes():
    """ Loads the heroes """
    global HEROES
    if HEROES is None:
        logger.info("Loading hero list from https://api.opendota.com/api/heroes")
        data = requests.get("https://api.opendota.com/api/heroes").json()
        HEROES = dict((d["id"], dict(d, index=i)) for (i, d) in enumerate(data))


class Hero():
    """ Hero data from the OpenDota heroes endpoint.  
    Sends request to API endpoint only when data is needed.  

    API reference: https://docs.opendota.com/#tag/heroes

    Args:
        hero_id (int): The hero ID
    """
    def __init__(self, hero_id):
        _load_heroes()
        self.hero = HEROES.get(int(hero_id))
        
        # Populate fields with None
        self._id = hero_id
        self._matches = None
        self._matchups = None
        self._durations = None
        self._players = None

    def __str__(self):
        """ Print format """
        return f"<Hero: {self._id} {self.name}>"

    @property
    def info(self):
        """ Returns a printable string of attributes """
        return (f"Hero id: {self.id}\n"
                f"name: {self.name}\n"
                f"localized_name: {self.localized_name}\n"
                f"primary_attr: {self.primary_attr}\n"
                f"attack_type: {self.attack_type}\n"
                f"roles: {self.roles}\n"
                f"legs: {self.legs}\n"
                f"thumbnail: {self.thumbnail}\n"
                f"thumbnail_small: {self.thumbnail_small}\n"
                f"url: {self.url}")

    @property
    def id(self):
        """ (int) Hero ID """
        return self._id

    @property
    def hero_id(self):
        """ (int) Hero ID """
        return self._id

    @property
    def name(self):
        """ (str) Hero name ('npc_dota_hero_anti_mage') """
        return self.hero.get('name')

    @property
    def localized_name(self):
        """ (str) Localized hero name ('Anti-Mage') """
        return self.hero.get('localized_name')

    @property
    def primary_attr(self):
        """ (str) Primary attribute ('agi', 'int', or 'str') """
        return self.hero.get('primary_attr')

    @property
    def attack_type(self):
        """ (str) Attack Type ('Melee' or 'Ranged') """
        return self.hero.get('attack_type')

    @property
    def roles(self):
        """ (list) Hero Roles (['Carry', 'Escape', 'Nuker']) """ 
        return self.hero.get('roles')

    @property
    def legs(self):
        """ (int) Number of hero's legs """
        return self.hero.get('legs')

    @property
    def thumbnail(self):
        """ (str) URL of a 235x272 thumbnail """
        return ("https://api.opendota.com/apps/dota2/images/heroes/"
                f"{self.name[14:]}_vert.jpg")

    @property
    def thumbnail_small(self):
        """ (str) URL of a 59x33 thumbnail """
        return ("https://api.opendota.com/apps/dota2/images/heroes/"
                f"{self.name[14:]}_sb.png")

    @property
    def url(self):
        """ (str) URL to the hero on opendota.com """
        return f"https://www.opendota.com/heroes/{self.id}"

    @property
    def matches(self):
        """ (list) Get recent matches for the hero

        https://docs.opendota.com/#tag/heroes%2Fpaths%2F~1heroes~1%7Bhero_id%7D~1matches%2Fget
        
        Returns a list of Match objects with the following attributes set:  
            (int)  match_id  
            (int)  start_time  
            (int)  duration  
            (bool) radiant_win  
            (int)  league_id  
            (str)  league_name  

        Along with the following player specific attributes:
            (int)  player_slot  
            (int)  account_id  
            (int)  kills  
            (int)  deaths  
            (int)  assists  
            (bool) radiant  
        """
        from .match import Match
        if not self._matches:
            logger.info(f"Loading matches for %s", self.localized_name)
            url = f"https://api.opendota.com/api/heroes/{self.id}/matches"
            data = requests.get(url).json()
            self._matches = []
            for item in data:
                match = Match(item.get("match_id"))

                # Player specific attributes
                match.player_slot = item.get("player_slot")
                match.account_id = item.get("account_id")
                match.kills = item.get("kills")
                match.deaths = item.get("deaths")
                match.assists = item.get("assists")
                match.radiant = item.get("radiant")
                match.league_name = item.get("league_name")

                # Private attributes (properties)
                match._id = item.get("match_id")
                match._match_id = item.get("match_id")
                match._start_time = item.get("start_time")
                match._duration = item.get("duration")
                match._radiant_win = item.get("radiant_win")
                match._league_id = item.get("leagueid")

                self._matches.append(match)
                
        return self._matches

    @property
    def matchups(self):
        """ (list) Get results against other heroes for the hero.
        
        https://docs.opendota.com/#tag/heroes%2Fpaths%2F~1heroes~1%7Bhero_id%7D~1matchups%2Fget
        
        Returns a list of dicts with the keys:  
            (int) hero_id  
            (int) games_played  
            (int) wins
        """
        if not self._matchups:
            logger.info(f"Loading matchups with %s", self.localized_name)
            url = f"https://api.opendota.com/api/heroes/{self.id}/matchups"
            self._matchups = requests.get(url).json()
        return self._matchups

    @property
    def durations(self):
        """ (list) Get recent durations with the hero.

        https://docs.opendota.com/#tag/heroes%2Fpaths%2F~1heroes~1%7Bhero_id%7D~1durations%2Fget
        
        Returns a list of dicts with the keys:  
            (int) duration_bin  
            (int) games_played  
            (int) wins  
        """
        if not self._durations:
            logger.info(f"Loading durations for %s", self.localized_name)
            url = f"https://api.opendota.com/api/heroes/{self.id}/durations"
            self._durations = requests.get(url).json()
        return self._durations

    @property
    def players(self):
        """ (list) Get recent players with the hero.
        
        https://docs.opendota.com/#tag/heroes%2Fpaths%2F~1heroes~1%7Bhero_id%7D~1players%2Fget

        Returns a list of Player objects with the following attributes set:  
            (int) player.id  
            (int) player.games_played  
            (int) player.hero_wins
        """
        from .player import Player
        if not self._players:
            logger.info(f"Loading players for %s", self.localized_name)
            url = f"https://api.opendota.com/api/heroes/{self.id}/players"
            data = requests.get(url).json()
            self._players = []
            for item in data:
                player = Player(item.get("account_id"))
                player.games_played = item.get("games_played")
                player.hero_wins = item.get("wins")
                self._players.append(player)

        return self._players
