import os
from gym import spaces
from .nes_env import NESEnv


class SuperMarioBrosEnv(NESEnv):
    """An environment for playing Super Mario Bros with OpenAI Gym."""

    def __init__(self,
        rom_mode: str=None,
        target_world: int=None,
        target_level: int=None,
        lost_levels: bool=False,
        **kwargs
    ) -> None:
        """
        Initialize a new Super Mario Bros environment.

        Args:
            rom_mode: the ROM mode to use when loading ROMs from disk. valid
                options are:
                -  None: the standard ROM with no modifications
                - 'downsample': down-sampled ROM with static artifacts removed
                - 'pixel': a simpler pixelated version of graphics
                - 'rectangle': an even simpler rectangular version of graphics

        Returns:
            None

        """
        super().__init__(**kwargs)
        # load the package directory of this class
        package_directory = os.path.dirname(os.path.abspath(__file__))
        # setup the path to the Lua script
        lua_name = 'lua/super-mario-bros.lua'
        self.lua_interface_path = os.path.join(package_directory, lua_name)
        # setup the path to the game ROM
        if lost_levels:
            if rom_mode is None:
                rom_name = 'roms/super-mario-bros-2.nes'
            elif rom_mode == 'pixel':
                raise ValueError('pixel_rom not supported for Lost Levels')
            elif rom_mode == 'rectangle':
                raise ValueError('rectangle_rom not supported for Lost Levels')
            elif rom_mode == 'downsample':
                rom_name = 'roms/super-mario-bros-2-downsampled.nes'
            else:
                raise ValueError('invalid rom_mode: {}'.format(repr(rom_mode)))
        else:
            if rom_mode is None:
                rom_name = 'roms/super-mario-bros.nes'
            elif rom_mode == 'pixel':
                rom_name = 'roms/super-mario-bros-pixel.nes'
            elif rom_mode == 'rectangle':
                rom_name = 'roms/super-mario-bros-rect.nes'
            elif rom_mode == 'downsample':
                rom_name = 'roms/super-mario-bros-downsampled_nobg.nes'
            elif rom_mode == 'nobg':
                rom_name = 'roms/super-mario-bros-downsampled.nes'
            else:
                raise ValueError('invalid rom_mode: {}'.format(repr(rom_mode)))
        # convert the path to an absolute path
        self.rom_file_path = os.path.join(package_directory, rom_name)
        # setup the discrete action space for the agent
        self.actions = [
            '',    # NOP
            # 'U',   # Up
            # 'D',   # Down
            'L',   # Left
            'R',   # Right
            'LA',  # Left + A (jump)
            'LB',  # Left + B (sprint)
            'LAB', # Left + A + B (sprint + jump)
            'RA',  # Right + A (jump)
            'RB',  # Right + B (sprint)
            'RAB', # Right + A + B (sprint + jump)
            'A',   # A
            # 'B',   # B
            # 'AB'   # A + B
        ]
        self.action_space = spaces.Discrete(len(self.actions))
        # setup the environment variables for the target levels
        os.environ['lost_levels'] = str(int(lost_levels))
        os.environ['target_world'] = str(target_world)
        os.environ['target_level'] = str(target_level)

    def get_keys_to_action(self) -> dict:
        """Return the dictionary of keyboard keys to actions."""
        # Mapping of buttons on the NES joy-pad to keyboard keys
        up =    ord('w')
        down =  ord('s')
        left =  ord('a')
        right = ord('d')
        A =     ord('o')
        B =     ord('p')
        # A mapping of pressed key combinations to discrete actions in action space
        keys_to_action = {
            (): 0,
            # (up, ): 1,
            # (down, ): 2,
            (left, ): 3,
            (right, ): 4,
            tuple(sorted((left, A, ))): 5,
            tuple(sorted((left, B, ))): 6,
            tuple(sorted((left, A, B, ))): 7,
            tuple(sorted((right, A, ))): 8,
            tuple(sorted((right, B, ))): 9,
            tuple(sorted((right, A, B, ))): 10,
            (A, ): 11,
            # (B, ): 12,
            # tuple(sorted((A, B))): 13
        }

        return keys_to_action


__all__ = [SuperMarioBrosEnv.__name__]
