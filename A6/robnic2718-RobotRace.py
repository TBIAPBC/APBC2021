from game_utils import nameFromPlayerId
from game_utils import Direction as D, MoveStatus
from game_utils import Tile, TileStatus, TileObject
from game_utils import Map, Status
from simulator import Simulator
from player_base import Player
import robnic_toolbox as toolbox

class ROBNIC(Player):
    def __init__(self):
        self.player_name = "Nicolas"
        pass
    
    def reset(self, player_id, max_players, width, height):
        self.map_width = width
        self.map_height = height
        self.max_players = max_players
        pass

    def round_begin(self, r):
        pass

    def move(self, status):
        # the status object (see game_utils.Status) contains:
        # - .player, our id, if we should have forgotten it
        # - .x and .y, our position
        # - .health and .gold, how much health and gold we have
        # - .map, a map of what we can see (see game_utils.Map)
        #   The origin of the map is in the lower left corner.
        # - .goldPots, a dict from positions to amounts
        # print("-" * 80)
        # print("Status for %s" % self.player_name)
        # # print the map as we can see it, along with health and gold
        # print(status)
        #print(status.map)  # the map can be printed too, but printing the status does this as well
        # for illustration, we go through the map and find stuff
        # A tile has a 'status' and an object 'obj'.
        # See game_utils.TileStatus and game_utils.TileObject
        pass

    def set_mines(self, stats):
        """
		Called to ask the player to set mines

		@param self the Player itself
		@param status the status
		@returns list of coordinates on the board

		The player answers with a list of positions, where mines
		should be set.
		"""
        pass

players = [ROBNIC()]