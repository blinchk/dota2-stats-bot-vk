import logging
import requests
from sys import stdout

logger = logging.getLogger(__name__)
#out_hdlr = logging.StreamHandler(stdout)
#out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
#out_hdlr.setLevel(logging.INFO)
#logger.addHandler(out_hdlr)
#logger.setLevel(logging.INFO)

class Match():
    """ Match data from the OpenDota matches endpoint.
    Sends request to API endpoint only when data is needed.

    API reference: https://docs.opendota.com/#tag/matches

    Args:
        match_id (int): The match ID
    """
    def __init__(self, match_id):
        self._id = int(match_id)
        self._loaded = False  # has the endpoint been called yet

        # Populate fields with None
        self._all_word_counts = None
        self._barracks_status_dire = None
        self._barracks_status_radiant = None
        self._chat = None
        self._cluster = None
        self._comeback = None
        self._cosmetics = None
        self._dire_score = None
        self._dire_team = None
        self._draft_timings = None
        self._duration = None
        self._engine = None
        self._first_blood_time = None
        self._game_mode = None
        self._human_players = None
        self._league = None
        self._league_id = None
        self._lobby_type = None
        self._loss = None
        self._match_seq_num = None
        self._my_word_counts = None
        self._negative_votes = None
        self._objectives = None
        self._patch = None
        self._picks_bans = None
        self._players = None
        self._positive_votes = None
        self._radiant_gold_adv = None
        self._radiant_score = None
        self._radiant_team = None
        self._radiant_win = None
        self._radiant_xp_adv = None
        self._region = None
        self._replay_salt = None
        self._replay_url = None
        self._series_id = None
        self._series_type = None
        self._skill = None
        self._start_time = None
        self._teamfights = None
        self._throw = None
        self._tower_status_dire = None
        self._tower_status_radiant = None
        self._version = None
        self._win = None

    def __str__(self):
        """ Print format """
        return f"<Match: {self._id}>"

    @property
    def info(self):
        """ Returns a printable string of attributes """
        return (f"Match id: {self._id}\n"
                f"dire_score: {self.dire_score}\n"
                f"dire_team: {self.dire_team}\n"
                f"duration: {self.duration}\n"
                f"game_mode: {self.game_mode}\n"
                f"patch: {self.patch}\n"
                f"radiant_score: {self.radiant_score}\n"
                f"radiant_team: {self.radiant_team}\n"
                f"radiant_win: {self.radiant_win}\n"
                f"skill: {self.skill}\n"
                f"start_time: {self.start_time}\n")

    def _load(self):
        """ Loads the match data from the endpoint.
        Called automatically when an attribute is requested.
        """
        if not self._loaded:
            url = f"https://api.opendota.com/api/matches/{self.id}"
            logger.info("Loading match details for match id: %s from url %s",
                        self._id, url)
            self.data = requests.get(url).json()
            self._duration                = self.data.get('duration')
            self._chat                    = self.data.get('chat')
            self._cluster                 = self.data.get('cluster')
            self._engine                  = self.data.get('engine')
            self._first_blood_time        = self.data.get('first_blood_time')
            self._game_mode               = self.data.get('game_mode')
            self._human_players           = self.data.get('human_players')
            self._league_id               = self.data.get('league_id')
            self._lobby_type              = self.data.get('lobby_type')
            self._match_seq_num           = self.data.get('match_seq_num')
            self._negative_votes          = self.data.get('negative_votes')
            self._positive_votes          = self.data.get('positive_votes')
            self._objectives              = self.data.get('objectives')
            self._picks_bans              = self.data.get('picks_bans')
            self._barracks_status_dire    = self.data.get('barracks_status_dire')
            self._dire_score              = self.data.get('dire_score')
            self._dire_team               = self.data.get('dire_team')
            self._tower_status_dire       = self.data.get('tower_status_dire')
            self._barracks_status_radiant = self.data.get('barracks_status_radiant')
            self._radiant_gold_adv        = self.data.get('radiant_gold_adv')
            self._radiant_xp_adv          = self.data.get('radiant_xp_adv')
            self._radiant_score           = self.data.get('radiant_score')
            self._radiant_team            = self.data.get('radiant_team')
            self._radiant_win             = self.data.get('radiant_win')
            self._tower_status_radiant    = self.data.get('tower_status_radiant')
            self._start_time              = self.data.get('start_time')
            self._teamfights              = self.data.get('teamfights')
            self._version                 = self.data.get('version')
            self._replay_salt             = self.data.get('replay_salt')
            self._series_id               = self.data.get('series_id')
            self._series_type             = self.data.get('series_type')
            self._league                  = self.data.get('league')
            self._skill                   = self.data.get('skill')
            self._players                 = self.data.get('players')
            self._patch                   = self.data.get('patch')
            self._region                  = self.data.get('region')
            self._all_word_counts         = self.data.get('all_word_counts')
            self._version                 = self.data.get('version')
            self._throw                   = self.data.get('throw')
            self._comeback                = self.data.get('comeback')
            self._cosmetics               = self.data.get('cosmetics')
            self._draft_timings           = self.data.get('draft_timings')
            self._loss                    = self.data.get('loss')
            self._win                     = self.data.get('win')
            self._replay_url              = self.data.get('replay_url')
            self._loaded = True

    def _get(self, key):
        """ Loads data if missing before getting an attribute """
        try:
            val = getattr(self, f"_{key}")
            if val is not None:
                return val
            else:
                self._load()
                return getattr(self, f"_{key}")
        except AttributeError:
            return None

    @property
    def id(self):
        """ (int) The ID number of the match assigned by Valve. """
        return self._id

    @property
    def match_id(self):
        """ (int) The ID number of the match assigned by Valve. """
        return self._id

    @property
    def chat(self):
        """ (list) Information on the chat of the game. 

        Returns a list of dicts like the following:  
            {'time': 318, 'type': 'chatwheel', 'key': '90', 'slot': 2, 'player_slot': 2}  
            {'time': 2013, 'type': 'chat', 'unit': '"plomdawg"', 'key': 'GG', 'slot': 6, 'player_slot': 129}  
        """
        return self._get("chat")

    @property
    def cluster(self):
        """ (int) Cluster number. """
        return self._get("cluster")

    @property
    def cosmetics(self):
        """ Cosmetics information.

        Returns a dict like:  
            {'647': 132, '4176': 132, '4468': 0, '5070': 1}
        """
        return self._get("cosmetics")

    @property
    def draft_timings(self):
        """ (list) Information on the draft timings during picking phase. """
        return self._get("draft_timings")

    @property
    def duration(self):
        """ (int) Duration of the match in seconds """
        return self._get("duration")

    @property
    def engine(self):
        """ (int) Engine version """
        return self._get("engine")

    @property
    def first_blood_time(self):
        """ (int) Time in seconds at which first blood occurred """
        return self._get("first_blood_time")

    @property
    def game_mode(self):
        """ (int) Game mode played.

        Game Modes:
            0:  "game_mode_unknown"  
            1:  "game_mode_all_pick"  
            2:  "game_mode_captains_mode"  
            3:  "game_mode_random_draft"  
            4:  "game_mode_single_draft"  
            5:  "game_mode_all_random"  
            6:  "game_mode_intro"  
            7:  "game_mode_diretide"  
            8:  "game_mode_reverse_captains_mode"  
            9:  "game_mode_greeviling"  
            10: "game_mode_tutorial"  
            11: "game_mode_mid_only"  
            12: "game_mode_least_played"  
            13: "game_mode_limited_heroes"  
            14: "game_mode_compendium_matchmaking"  
            15: "game_mode_custom"  
            16: "game_mode_captains_draft"  
            17: "game_mode_balanced_draft"  
            18: "game_mode_ability_draft"  
            19: "game_mode_event"  
            20: "game_mode_all_random_death_match"  
            21: "game_mode_1v1_mid"  
            22: "game_mode_all_draft"  
            23: "game_mode_turbo"  
            24: "game_mode_mutation"  
        """
        return self._get("game_mode")

    @property
    def human_players(self):
        """ Number of human players in the game """
        return self._get("human_players")

    @property
    def league_id(self):
        """ (int) League ID """
        return self._get("league_id")

    @property
    def lobby_type(self):
        """ (int) Lobby type of match.

        Lobby Types:  
            0: "lobby_type_normal"  
            1: "lobby_type_practice"  
            2: "lobby_type_tournament"  
            3: "lobby_type_tutorial"  
            4: "lobby_type_coop_bots"  
            5: "lobby_type_ranked_team_mm"  
            6: "lobby_type_ranked_solo_mm"  
            7: "lobby_type_ranked"  
            8: "lobby_type_1v1_mid"  
            9: "lobby_type_battle_cup"
        """
        return self._get("lobby_type")

    @property
    def match_seq_num(self):
        """ (int) Match sequence number """
        return self._get("match_seq_num")

    @property
    def negative_votes(self):
        """ (int) Number of negative votes the replay received """
        return self._get("negative_votes")

    @property
    def positive_votes(self):
        """ (int) Number of positive votes the replay received """
        return self._get("positive_votes")

    @property
    def objectives(self):
        """ (list) Objectives. 
        
        Returns a list of objectives like:  
            {'time': 70, 'type': 'CHAT_MESSAGE_FIRSTBLOOD', 'slot': 0, 'key': 8, 'player_slot': 0} 
            {'time': 1930, 'type': 'CHAT_MESSAGE_ROSHAN_KILL', 'team': 3}  
        """
        return self._get("objectives")

    @property
    def picks_bans(self):
        """ Object containing information on the draft.
        Each pick/ban contains a boolean relating to whether
        the choice is a pick or a ban, the hero ID, the team
        the picked or banned it, and the order.
        """
        return self._get("picks_bans")

    # Dire stats
    @property
    def barracks_status_dire(self):
        """	int: Bitmask. An integer that represents a binary of
        which barracks are still standing. 63 would mean all barracks
        still stand at the end of the game."""
        return self._get("barracks_status_dire")

    @property
    def dire_score(self):
        """ Final score for Dire (# kills on Radiant) """
        return self._get("dire_score")

    @property
    def dire_team(self):
        """ Dire team """
        return self._get("dire_team")

    @property
    def tower_status_dire(self):
        """ Bitmask. An integer that represents a binary
        of which Dire towers are still standing."""
        return self._get("tower_status_dire")

    # Radiant stats
    @property
    def barracks_status_radiant(self):
        """	int: Bitmask. An integer that represents a binary of
        which barracks are still standing. 63 (0b111111) would mean 
        all barracks still stand at the end of the game."""
        return self._get("barracks_status_radiant")

    @property
    def radiant_gold_adv(self):
        """ List of the Radiant gold advantage at each minute in the game. """
        return self._get("radiant_gold_adv")

    @property
    def radiant_xp_adv(self):
        """ List of the Radiant xp advantage at each minute in the game. """
        return self._get("radiant_xp_adv")

    @property
    def radiant_score(self):
        """ Final score for Radiant (# kills on Dire) """
        return self._get("radiant_score")

    @property
    def radiant_team(self):
        """ Radiant team """
        return self._get("radiant_team")

    @property
    def radiant_win(self):
        """ Boolean indicating whether Radiant won the match """
        return self._get("radiant_win")

    @property
    def tower_status_radiant(self):
        """ Bitmask. An integer that represents a binary
        of which Radiant towers are still standing."""
        return self._get("tower_status_radiant")

    @property
    def start_time(self):
        """ The Unix timestamp at which the game started """
        return self._get("start_time")

    @property
    def teamfights(self):
        """ List of teamfights """
        return self._get("teamfights")

    @property
    def version(self):
        """ Parse version, used internally by OpenDota """
        return self._get("version")

    @property
    def replay_salt(self):
        """ Replay salt """
        return self._get("replay_salt")

    @property
    def series_id(self):
        """ Series ID """
        return self._get("series_id")

    @property
    def series_type(self):
        """ Series type """
        return self._get("series_type")

    @property
    def league(self):
        """ League ? """
        return self._get("league")

    @property
    def skill(self):
        """ Skill bracket assigned by Valve (Normal, High, Very High) """
        return self._get("skill")

    @property
    def players(self):
        """ List of info on individual players """
        return self._get("players")

    @property
    def patch(self):
        """ Parse version, used internally by OpenDota """
        return self._get("patch")

    @property
    def region(self):
        """ Integer corresponding to the region the game was played on """
        return self._get("region")

    @property
    def all_word_counts(self):
        """ Word counts of the all chat messages in the player's games """
        return self._get("all_word_counts")

    @property
    def my_word_counts(self):
        """ Word counts of the player's all chat messages """
        return self._get("version")

    @property
    def throw(self):
        """ Maximum gold advantage of the player's team if they lost """
        return self._get("throw")

    @property
    def comeback(self):
        """ Maximum gold disadvantage of the player's team if they won """
        return self._get("comeback")

    @property
    def loss(self):
        """ Maximum gold disadvantage of the player's team if they lost """
        return self._get("loss")

    @property
    def win(self):
        """ Maximum gold advantage of the player's team if they won """
        return self._get("win")

    @property
    def replay_url(self):
        """ Replay download URL """
        return self._get("replay_url")

    @property
    def url(self):
        """ Match URL on opendota.com """
        return f"https://www.opendota.com/matches/{self._id}"
