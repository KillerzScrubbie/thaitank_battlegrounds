import webbrowser

# Try importing the module. If there is no module, raise an error and ask for the user to download.
try:
    from arcade.gui import *
    from gamedata import *
except ModuleNotFoundError:
    webbrowser.open("http://arcade.academy/installation.html")
    print("Try following the installation of arcade module on this website.\n"
          "By downloading all the files directly from GitHub will give you the latest version possible of arcade.\n"
          "Or if you are using PyCharm, follow the steps below.")

    print("How to run the game first time on PyCharm\n"
          "1. Open up preference in PyCharm\n"
          "2. Search for arcade module\n"
          "3. Download arcade module 2.1.6 (Tested with 2.1.6, 2.1.7 is not compatible due to a bug)\n"
          "4. Try running this program again")
    exit(0)

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "ThaiTank BattleGrounds"


class PlayButton(TextButton):
    def __init__(self, game, x=0, y=0, width=100, height=40, text="", theme=None):
        super().__init__(x, y, width, height, text, 24, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True
        arcade.play_sound(sound_click_button)

    def on_release(self):
        if self.pressed:
            self.pressed = False
            self.game.next_menu = True


class QuitButton(TextButton):
    def __init__(self, game, x=0, y=0, width=100, height=40, text="", theme=None):
        super().__init__(x, y, width, height, text, 24, theme=theme)
        self.game = game

    def on_press(self):
        self.pressed = True
        arcade.play_sound(sound_click_button)

    def on_release(self):
        if self.pressed:
            exit(0)


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.next_menu = False
        self.theme = None
        self.theme2 = None
        self.background = None

    def setup(self):
        self.setup_theme()
        self.set_buttons()
        self.background = arcade.load_texture("assets/screens/mainmenu.png")

    def set_buttons(self):
        self.button_list.append(PlayButton(self, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75, 400, 100, theme=self.theme))
        self.button_list.append(QuitButton(self, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-200, 400, 100, theme=self.theme2))

    def setup_theme(self):
        self.theme = Theme()
        self.theme2 = Theme()
        self.set_play_button_textures()
        self.set_quit_button_textures()

    def set_play_button_textures(self):
        normal = "assets/customui/yellow_button00.png"
        hover = "assets/customui/yellow_button01.png"
        clicked = "assets/customui/yellow_button02.png"
        locked = "assets/customui/yellow_button03.png"
        self.theme.add_button_textures(normal, hover, clicked, locked)

    def set_quit_button_textures(self):
        normal = "assets/customui/quit_button0.png"
        hover = "assets/customui/quit_button1.png"
        clicked = "assets/customui/quit_button2.png"
        locked = "assets/customui/quit_button3.png"
        self.theme2.add_button_textures(normal, hover, clicked, locked)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        super().on_draw()

    def on_update(self, delta_time: float):
        if self.next_menu:
            instructions_view = InstructionView()
            instructions_view.setup()
            self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None

    def setup(self):
        self.background = arcade.load_texture("assets/screens/tutorial1.png")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        arcade.play_sound(sound_click_button)
        next_view = InstructionView2()
        next_view.setup()
        self.window.show_view(next_view)


class InstructionView2(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None

    def setup(self):
        self.background = arcade.load_texture("assets/screens/tutorial2.png")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        arcade.play_sound(sound_click_button)
        next_view = InstructionView3()
        next_view.setup()
        self.window.show_view(next_view)


class InstructionView3(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None

    def setup(self):
        self.background = arcade.load_texture("assets/screens/tutorial3.png")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        arcade.play_sound(sound_click_button)
        game_view = MainGame()
        game_view.setup()
        self.window.show_view(game_view)


class MainGame(arcade.View):
    """ Main application class """

    def __init__(self):

        # Set up the window
        super().__init__()
        arcade.set_background_color(arcade.csscolor.LIGHT_SKY_BLUE)

        # Player Sprites
        self.player_sprite = None
        self.player_sprite2 = None

        # Sprite lists
        self.wall_list = None
        self.player_list = None
        self.base_list = None
        self.bullet_list = None
        self.enemy_list = None
        self.enemy_bullet_list = None
        self.missile_list = None
        self.hud_list = None

        # Explosion animation list.
        self.explosion_texture_list = None
        self.smoke_texture_list = None

        # Map lists
        self.background_list = None
        self.decor_list = None
        self.decor2_list = None
        self.spawn_list = None
        self.number_list = None

        self.spawns = []

        # All sprites
        self.all_sprites_list = None

        # Set up better movement style
        # Player 1
        self.left_pressed = False
        self.up_pressed = False
        self.right_pressed = False
        self.down_pressed = False
        # Player 2
        self.left_pressed2 = False
        self.up_pressed2 = False
        self.right_pressed2 = False
        self.down_pressed2 = False

        # Game state
        self.game_over = False
        self.idle_timer = 270
        self.wave = 0
        self.between_wave = True
        self.next_wave_ready = False
        self.win = False

        # Player HUD
        self.player1_HUD = None
        self.player2_HUD = None

        self.wave_on_screen_HUD = []
        self.wave_HUD = []

        self.p1_hp_HUD = []
        self.p1_dmg_HUD = []
        self.p1_speed_HUD = []
        self.p1_rotate_HUD = []
        self.p1_bullet_HUD = []

        self.p2_hp_HUD = []
        self.p2_dmg_HUD = []
        self.p2_speed_HUD = []
        self.p2_rotate_HUD = []
        self.p2_bullet_HUD = []

        # Displaying HUD Sprites
        self.wave_hud_display = None

        self.p1_hp_HUD_display = None
        self.p1_dmg_HUD_display = None
        self.p1_speed_HUD_display = None
        self.p1_rotate_HUD_display = None
        self.p1_bullet_HUD_display = None

        self.p2_hp_HUD_display = None
        self.p2_dmg_HUD_display = None
        self.p2_speed_HUD_display = None
        self.p2_rotate_HUD_display = None
        self.p2_bullet_HUD_display = None

        # Player upgrade levels
        self.player1_hp_lvl = 0
        self.player1_dmg_lvl = 0
        self.player1_speed_lvl = 0
        self.player1_rotate_speed_lvl = 0
        self.player1_bullet_speed_lvl = 0

        self.player2_hp_lvl = 0
        self.player2_dmg_lvl = 0
        self.player2_speed_lvl = 0
        self.player2_rotate_speed_lvl = 0
        self.player2_bullet_speed_lvl = 0

    def call_next_wave(self):
        self.wave += 1
        self.idle_timer = 0
        self.between_wave = False

    def finish_wave(self):
        """ After a wave is finished, this function will be called. """
        self.idle_timer = -1
        self.between_wave = True
        self.next_wave_ready = False

        # Clear enemies' bullets
        for bullet in self.enemy_bullet_list:
            bullet.kill()

        # Respawn dead players
        self.respawn_player()

        # Add a skill point and fully heal all players
        for player in self.player_list:
            player.skill_point += 1
            player.health = player.max_health

    def respawn_player(self):
        """ Respawn the players. """
        if self.player_sprite.health == 0:
            self.player_sprite = Tank(self.spawns[0], "assets/tanks/tank_green.png")
            self.player_list.append(self.player_sprite)
            self.all_sprites_list.append(self.player_sprite)
            self.player_sprite.respawn(self.player1_hp_lvl, self.player1_dmg_lvl, self.player1_speed_lvl,
                                       self.player1_rotate_speed_lvl, self.player1_bullet_speed_lvl)
        elif self.player_sprite2.health == 0:
            self.player_sprite2 = Tank(self.spawns[1], "assets/tanks/tank_red.png")
            self.player_list.append(self.player_sprite2)
            self.all_sprites_list.append(self.player_sprite2)
            self.player_sprite2.respawn(self.player2_hp_lvl, self.player2_dmg_lvl, self.player2_speed_lvl,
                                        self.player2_rotate_speed_lvl, self.player2_bullet_speed_lvl)

    def setup(self):
        """ Set up the game and initialize the variables """

        # Sprite lists
        self.wall_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.base_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()
        self.missile_list = arcade.SpriteList()
        self.hud_list = arcade.SpriteList()

        # Load in HUD texture into lists.
        for level in range(5):
            p1_hp = f"assets/hud/p1_hp_lvl{level+1}.png"
            self.p1_hp_HUD.append(arcade.load_texture(p1_hp))
            p1_hp_ready = f"assets/hud/p1_hp_lvl{level + 1}_ready.png"
            self.p1_hp_HUD.append(arcade.load_texture(p1_hp_ready))
            p1_dmg = f"assets/hud/p1_dmg_lvl{level + 1}.png"
            self.p1_dmg_HUD.append(arcade.load_texture(p1_dmg))
            p1_dmg_ready = f"assets/hud/p1_dmg_lvl{level + 1}_ready.png"
            self.p1_dmg_HUD.append(arcade.load_texture(p1_dmg_ready))

            p2_hp = f"assets/hud/p2_hp_lvl{level + 1}.png"
            self.p2_hp_HUD.append(arcade.load_texture(p2_hp))
            p2_hp_ready = f"assets/hud/p2_hp_lvl{level + 1}_ready.png"
            self.p2_hp_HUD.append(arcade.load_texture(p2_hp_ready))
            p2_dmg = f"assets/hud/p2_dmg_lvl{level + 1}.png"
            self.p2_dmg_HUD.append(arcade.load_texture(p2_dmg))
            p2_dmg_ready = f"assets/hud/p2_dmg_lvl{level + 1}_ready.png"
            self.p2_dmg_HUD.append(arcade.load_texture(p2_dmg_ready))

        for level in range(4):
            p1_speed = f"assets/hud/p1_speed_lvl{level + 1}.png"
            self.p1_speed_HUD.append(arcade.load_texture(p1_speed))
            p1_speed_ready = f"assets/hud/p1_speed_lvl{level + 1}_ready.png"
            self.p1_speed_HUD.append(arcade.load_texture(p1_speed_ready))
            p1_rotate = f"assets/hud/p1_rotate_lvl{level + 1}.png"
            self.p1_rotate_HUD.append(arcade.load_texture(p1_rotate))
            p1_rotate_ready = f"assets/hud/p1_rotate_lvl{level + 1}_ready.png"
            self.p1_rotate_HUD.append(arcade.load_texture(p1_rotate_ready))
            p1_bullet = f"assets/hud/p1_bullet_lvl{level + 1}.png"
            self.p1_bullet_HUD.append(arcade.load_texture(p1_bullet))
            p1_bullet_ready = f"assets/hud/p1_bullet_lvl{level + 1}_ready.png"
            self.p1_bullet_HUD.append(arcade.load_texture(p1_bullet_ready))

            p2_speed = f"assets/hud/p2_speed_lvl{level + 1}.png"
            self.p2_speed_HUD.append(arcade.load_texture(p2_speed))
            p2_speed_ready = f"assets/hud/p2_speed_lvl{level + 1}_ready.png"
            self.p2_speed_HUD.append(arcade.load_texture(p2_speed_ready))
            p2_rotate = f"assets/hud/p2_rotate_lvl{level + 1}.png"
            self.p2_rotate_HUD.append(arcade.load_texture(p2_rotate))
            p2_rotate_ready = f"assets/hud/p2_rotate_lvl{level + 1}_ready.png"
            self.p2_rotate_HUD.append(arcade.load_texture(p2_rotate_ready))
            p2_bullet = f"assets/hud/p2_bullet_lvl{level + 1}.png"
            self.p2_bullet_HUD.append(arcade.load_texture(p2_bullet))
            p2_bullet_ready = f"assets/hud/p2_bullet_lvl{level + 1}_ready.png"
            self.p2_bullet_HUD.append(arcade.load_texture(p2_bullet_ready))

        self.wave_on_screen_HUD.append(arcade.load_texture("assets/waves/waveFinished.png"))
        for wave in range(10):
            wave_hud = f"assets/hud/wave{wave+1}.png"
            self.wave_HUD.append(arcade.load_texture(wave_hud))
            wave_on_screen = f"assets/waves/wave{wave+1}.png"
            self.wave_on_screen_HUD.append(arcade.load_texture(wave_on_screen))

        # Explosion animation list.
        self.explosion_texture_list = []
        for explosion in range(EXPLOSION_TEXTURES):
            texture_name = f"assets/tanks/explosion{explosion+1}.png"
            self.explosion_texture_list.append(arcade.load_texture(texture_name))

        self.smoke_texture_list = []
        for smoke in range(EXPLOSION_TEXTURES):
            texture_name = f"assets/tanks/explosionSmoke{smoke+1}.png"
            self.smoke_texture_list.append(arcade.load_texture(texture_name))

        # Map lists
        self.background_list = arcade.SpriteList()
        self.decor_list = arcade.SpriteList()
        self.decor2_list = arcade.SpriteList()
        self.spawn_list = arcade.SpriteList()
        self.number_list = arcade.SpriteList()

        # A sprite list to be drawn.
        self.all_sprites_list = arcade.SpriteList()

        # Load in a map from tiled editor
        map_name = "map.tmx"

        # Assign the layers' name
        background_layer_name = "Background"
        decor_layer_name = "Decoration"
        decor2_layer_name = "Decoration2"
        spawn_layer_name = "Spawn"
        number_layer_name = "Number"

        # Read in the .tmx map
        desert_map = arcade.tilemap.read_tmx(map_name)

        self.background_list = arcade.tilemap.process_layer(desert_map, background_layer_name, TILE_SCALING)
        self.decor_list = arcade.tilemap.process_layer(desert_map, decor_layer_name, TILE_SCALING)
        self.decor2_list = arcade.tilemap.process_layer(desert_map, decor2_layer_name, TILE_SCALING)
        self.spawn_list = arcade.tilemap.process_layer(desert_map, spawn_layer_name, TILE_SCALING)
        self.number_list = arcade.tilemap.process_layer(desert_map, number_layer_name, TILE_SCALING)

        # Set up the player
        for coord in self.number_list:
            self.spawns.append(coord.position)

        # Players will start at the spawn point indicated by the number
        self.player_sprite = Tank(self.spawns[0], "assets/tanks/tank_green.png")
        self.player_sprite2 = Tank(self.spawns[1], "assets/tanks/tank_red.png")
        self.player_list.append(self.player_sprite)
        self.player_list.append(self.player_sprite2)
        self.all_sprites_list.append(self.player_sprite)
        self.all_sprites_list.append(self.player_sprite2)

        # Player HUD
        self.player1_HUD = TankHUD("assets/tanks/tank_green.png", 64)
        self.player2_HUD = TankHUD("assets/tanks/tank_red.png", 1856)

        self.hud_list.append(self.player1_HUD)
        self.hud_list.append(self.player2_HUD)

        self.p1_hp_HUD_display = HUD(self.p1_hp_HUD, 306)
        self.p1_dmg_HUD_display = HUD(self.p1_dmg_HUD, 421)
        self.p1_speed_HUD_display = HUD(self.p1_speed_HUD, 536)
        self.p1_rotate_HUD_display = HUD(self.p1_rotate_HUD, 651)
        self.p1_bullet_HUD_display = HUD(self.p1_bullet_HUD, 766)

        self.p2_hp_HUD_display = HUD(self.p2_hp_HUD, 1153)
        self.p2_dmg_HUD_display = HUD(self.p2_dmg_HUD, 1268)
        self.p2_speed_HUD_display = HUD(self.p2_speed_HUD, 1383)
        self.p2_rotate_HUD_display = HUD(self.p2_rotate_HUD, 1498)
        self.p2_bullet_HUD_display = HUD(self.p2_bullet_HUD, 1613)

        self.hud_list.append(self.p1_hp_HUD_display)
        self.hud_list.append(self.p1_dmg_HUD_display)
        self.hud_list.append(self.p1_speed_HUD_display)
        self.hud_list.append(self.p1_rotate_HUD_display)
        self.hud_list.append(self.p1_bullet_HUD_display)
        self.hud_list.append(self.p2_hp_HUD_display)
        self.hud_list.append(self.p2_dmg_HUD_display)
        self.hud_list.append(self.p2_speed_HUD_display)
        self.hud_list.append(self.p2_rotate_HUD_display)
        self.hud_list.append(self.p2_bullet_HUD_display)

        # Wave HUD
        self.wave_hud_display = HUD(self.wave_HUD, SCREEN_WIDTH/2)
        self.hud_list.append(self.wave_hud_display)

    def on_draw(self):
        """ Render the screen """
        arcade.start_render()

        # Draw the background
        self.background_list.draw()
        self.decor_list.draw()
        self.decor2_list.draw()
        self.spawn_list.draw()
        self.number_list.draw()

        # Draw all the sprites.
        self.all_sprites_list.draw()

        # Player HUD
        font = "AGENCYB"

        arcade.draw_rectangle_filled(110, 62, 150, 70, arcade.color.LIME_GREEN)
        arcade.draw_rectangle_filled(1810, 62, 150, 70, arcade.color.ROSSO_CORSA)

        arcade.draw_text(f"HP: {self.player_sprite.health}", 100, 66, arcade.color.BLACK, 20, font_name=font)
        arcade.draw_text(f"HP: {self.player_sprite2.health}", 1750, 66, arcade.color.BLACK, 20, font_name=font)

        arcade.draw_text(f"DMG: {self.player_sprite.damage}", 100, 36, arcade.color.BLACK, 20, font_name=font)
        arcade.draw_text(f"DMG: {self.player_sprite2.damage}", 1750, 36, arcade.color.BLACK, 20, font_name=font)

        self.hud_list.draw()

        # Enemy HP Indicator
        for enemy in self.enemy_list:
            arcade.draw_text(f"{enemy.health}", enemy.hp_x, enemy.hp_y, arcade.color.BLACK, 14, align="center",
                             anchor_x="center", anchor_y="center", font_name="AGENCYB")

        # Player ammo Indicator
        for player in self.player_list:
            if not player.reloading:
                arcade.draw_text(f"{player.ammo}", player.ammo_x, player.ammo_y, arcade.color.BLACK, 14, align="center",
                                 anchor_x="center", anchor_y="center", font_name="AGENCYB")
            else:
                arcade.draw_text(f"{player.reload_timer*10}%", player.ammo_x, player.ammo_y, arcade.color.STIZZA, 12,
                                 align="center", anchor_x="center", anchor_y="center", font_name="AGENCYB")

    def on_key_press(self, key, modifiers):
        """ Call whenever a key is pressed. """

        # If either the shoot button is pressed. It will call the shoot() from the respective player.
        if self.player_sprite.health > 0 and not self.player_sprite.reloading:  # Player 1
            if key == arcade.key.SPACE:
                bullet, flash = self.player_sprite.shoot("assets/tanks/bulletGreen1_outline.png")
                self.bullet_list.append(bullet)
                self.all_sprites_list.append(flash)
                self.all_sprites_list.append(bullet)
            elif key == arcade.key.R and self.player_sprite.ammo != 30:
                self.player_sprite.reload()

        if self.player_sprite2.health > 0 and not self.player_sprite2.reloading:  # Player 2
            if key == arcade.key.L:
                bullet, flash = self.player_sprite2.shoot("assets/tanks/bulletRed1_outline.png")
                self.bullet_list.append(bullet)
                self.all_sprites_list.append(flash)
                self.all_sprites_list.append(bullet)
            elif key == arcade.key.K and self.player_sprite2.ammo != 30:
                self.player_sprite2.reload()

        # Player 1 movement
        if key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.D:
            self.right_pressed = True

        # Player 2 movement
        if key == arcade.key.UP:
            self.up_pressed2 = True
        elif key == arcade.key.DOWN:
            self.down_pressed2 = True
        elif key == arcade.key.LEFT:
            self.left_pressed2 = True
        elif key == arcade.key.RIGHT:
            self.right_pressed2 = True

        # Miscellaneous
        if key == arcade.key.P:  # Pause
            pause = PauseView(self)
            # Disable movement upon pausing
            # Player 1
            self.left_pressed = False
            self.up_pressed = False
            self.right_pressed = False
            self.down_pressed = False
            # Player 2
            self.left_pressed2 = False
            self.up_pressed2 = False
            self.right_pressed2 = False
            self.down_pressed2 = False
            self.window.show_view(pause)

        # Player 1 upgrades
        if self.player_sprite.skill_point > 0:
            # Upgrade upon key pressed
            if key == arcade.key.KEY_1 and self.player1_hp_lvl < 4:
                self.player_sprite.upgrade_hp()
                self.player1_hp_lvl += 1
                self.p1_hp_HUD_display.level_up()
            elif key == arcade.key.KEY_2 and self.player1_dmg_lvl < 4:
                self.player_sprite.upgrade_damage()
                self.player1_dmg_lvl += 1
                self.p1_dmg_HUD_display.level_up()
            elif key == arcade.key.KEY_3 and self.player1_speed_lvl < 3:
                self.player_sprite.upgrade_speed()
                self.player1_speed_lvl += 1
                self.p1_speed_HUD_display.level_up()
            elif key == arcade.key.KEY_4 and self.player1_rotate_speed_lvl < 3:
                self.player_sprite.upgrade_rotate_speed()
                self.player1_rotate_speed_lvl += 1
                self.p1_rotate_HUD_display.level_up()
            elif key == arcade.key.KEY_5 and self.player1_bullet_speed_lvl < 3:
                self.player_sprite.upgrade_bullet_speed()
                self.player1_bullet_speed_lvl += 1
                self.p1_bullet_HUD_display.level_up()

        # Player 2 upgrades
        if self.player_sprite2.skill_point > 0:
            if key == arcade.key.KEY_6 and self.player2_hp_lvl < 4:
                self.player_sprite2.upgrade_hp()
                self.player2_hp_lvl += 1
                self.p2_hp_HUD_display.level_up()
            elif key == arcade.key.KEY_7 and self.player2_dmg_lvl < 4:
                self.player_sprite2.upgrade_damage()
                self.player2_dmg_lvl += 1
                self.p2_dmg_HUD_display.level_up()
            elif key == arcade.key.KEY_8 and self.player2_speed_lvl < 3:
                self.player_sprite2.upgrade_speed()
                self.player2_speed_lvl += 1
                self.p2_speed_HUD_display.level_up()
            elif key == arcade.key.KEY_9 and self.player2_rotate_speed_lvl < 3:
                self.player_sprite2.upgrade_rotate_speed()
                self.player2_rotate_speed_lvl += 1
                self.p2_rotate_HUD_display.level_up()
            elif key == arcade.key.KEY_0 and self.player2_bullet_speed_lvl < 3:
                self.player_sprite2.upgrade_bullet_speed()
                self.player2_bullet_speed_lvl += 1
                self.p2_bullet_HUD_display.level_up()

    def create_man(self, quantity=1):
        for i in range(quantity):
            enemy_sprite = Man()
            self.enemy_list.append(enemy_sprite)
            self.all_sprites_list.append(enemy_sprite)

    def create_woman(self, quantity=1):
        for i in range(quantity):
            enemy_sprite = Woman()
            self.enemy_list.append(enemy_sprite)
            self.all_sprites_list.append(enemy_sprite)

    def create_soldier(self, quantity=1):
        for i in range(quantity):
            enemy_sprite = Soldier()
            self.enemy_list.append(enemy_sprite)
            self.all_sprites_list.append(enemy_sprite)

    def create_enemy_tank(self, quantity=1):
        for i in range(quantity):
            enemy_sprite = EnemyTank()
            self.enemy_list.append(enemy_sprite)
            self.all_sprites_list.append(enemy_sprite)

    def create_massive_tank(self, quantity=1):
        for i in range(quantity):
            enemy_sprite = MassiveTank()
            self.enemy_list.append(enemy_sprite)
            self.all_sprites_list.append(enemy_sprite)

    def on_key_release(self, key, modifiers):
        """ Call whenever a key is released. """

        # Player 1 movement
        if key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.D:
            self.right_pressed = False

        # Player 2 movement
        if key == arcade.key.UP:
            self.up_pressed2 = False
        elif key == arcade.key.DOWN:
            self.down_pressed2 = False
        elif key == arcade.key.LEFT:
            self.left_pressed2 = False
        elif key == arcade.key.RIGHT:
            self.right_pressed2 = False

    def win(self):
        win_view = WinView()
        win_view.setup()
        self.window.show_view(win_view)

    def update(self, delta_time):
        """ Update all the sprites. """
        for player in self.player_list:
            if player.health < 0:
                player.health = 0

        # Increment idle timer by 1 in 1/60 sec.
        self.idle_timer += 1

        # Wave ended
        if len(self.enemy_list) == 0 and self.next_wave_ready:
            if self.wave < 10:
                self.finish_wave()
            else:
                self.win = True

        if self.between_wave:
            if self.idle_timer == -1:
                hud = WaveHUD(self.wave_on_screen_HUD)
                self.hud_list.append(hud)
            elif self.idle_timer == 240:
                self.wave_hud_display.next_lvl()
            elif self.idle_timer == 300:
                self.call_next_wave()
                hud = WaveHUD(self.wave_on_screen_HUD, self.wave)
                self.hud_list.append(hud)

        # Waves
        else:
            if self.wave == 1:
                # 30 Men
                if self.idle_timer == 2*SECOND:
                    self.create_man(2)
                elif self.idle_timer == 8*SECOND:
                    self.create_man(3)
                elif self.idle_timer == 12*SECOND:
                    self.create_man(5)
                elif self.idle_timer == 18*SECOND:
                    self.create_man(4)
                elif self.idle_timer == 22*SECOND:
                    self.create_man(6)
                elif self.idle_timer == 25*SECOND:
                    self.create_man(2)
                elif self.idle_timer == 27*SECOND:
                    self.create_man(2)
                elif self.idle_timer == 28*SECOND:
                    self.create_man(2)
                elif self.idle_timer == 29*SECOND:
                    self.create_man(2)
                elif self.idle_timer == 30*SECOND:
                    self.create_man(2)
                    self.next_wave_ready = True

            elif self.wave == 2:
                # 40 Men 20 Women
                if self.idle_timer == 2*SECOND:
                    self.create_man(5)
                elif self.idle_timer == 8*SECOND:
                    self.create_man(2)
                    self.create_woman()
                elif self.idle_timer == 12*SECOND:
                    self.create_man(3)
                    self.create_woman(3)
                elif self.idle_timer == 18*SECOND:
                    self.create_man(8)
                    self.create_woman(2)
                elif self.idle_timer == 22*SECOND:
                    self.create_man(6)
                    self.create_woman(4)
                elif self.idle_timer == 27*SECOND:
                    self.create_man(8)
                    self.create_woman(2)
                elif self.idle_timer == 30*SECOND:
                    self.create_man(5)
                elif self.idle_timer == 33*SECOND:
                    self.create_man(3)
                    self.create_woman(8)
                    self.next_wave_ready = True

            elif self.wave == 3:
                # 50 Men 40 Women 10 Soldiers
                if self.idle_timer == 3*SECOND:
                    self.create_man(10)
                    self.create_woman(4)
                elif self.idle_timer == 10*SECOND:
                    self.create_woman(3)
                    self.create_soldier()
                elif self.idle_timer == 15*SECOND:
                    self.create_man(5)
                    self.create_woman(2)
                elif self.idle_timer == 17*SECOND:
                    self.create_man(8)
                    self.create_woman(4)
                    self.create_soldier(2)
                elif self.idle_timer == 25*SECOND:
                    self.create_man(10)
                    self.create_woman(8)
                    self.create_soldier(2)
                elif self.idle_timer == 32*SECOND:
                    self.create_man(8)
                    self.create_woman(9)
                elif self.idle_timer == 38*SECOND:
                    self.create_man(4)
                    self.create_woman(5)
                elif self.idle_timer == 50*SECOND:
                    self.create_man(5)
                    self.create_woman(5)
                    self.create_soldier(5)
                    self.next_wave_ready = True

            elif self.wave == 4:
                # 35 Men 35 Women 40 Soldiers
                if self.idle_timer == 3*SECOND:
                    self.create_man(3)
                    self.create_woman(2)
                    self.create_soldier(3)
                elif self.idle_timer == 10*SECOND:
                    self.create_man(5)
                    self.create_woman(4)
                elif self.idle_timer == 12*SECOND:
                    self.create_soldier(10)
                elif self.idle_timer == 18*SECOND:
                    self.create_man(7)
                    self.create_woman(2)
                    self.create_soldier(3)
                elif self.idle_timer == 20*SECOND:
                    self.create_woman(8)
                    self.create_soldier(3)
                elif self.idle_timer == 25*SECOND:
                    self.create_man(10)
                    self.create_soldier(7)
                elif self.idle_timer == 30*SECOND:
                    self.create_man(5)
                    self.create_woman(10)
                elif self.idle_timer == 38*SECOND:
                    self.create_man(5)
                    self.create_woman(9)
                    self.create_soldier(14)
                    self.next_wave_ready = True

            elif self.wave == 5:
                # 20 Men 50 Women 30 Soldiers 10 Tanks
                if self.idle_timer == 2*SECOND:
                    self.create_woman(10)
                    self.create_soldier(6)
                elif self.idle_timer == 10*SECOND:
                    self.create_man(8)
                    self.create_woman(10)
                elif self.idle_timer == 13*SECOND:
                    self.create_man(5)
                    self.create_soldier(10)
                    self.create_enemy_tank(3)
                elif self.idle_timer == 20*SECOND:
                    self.create_man(3)
                    self.create_woman(10)
                    self.create_enemy_tank()
                elif self.idle_timer == 24*SECOND:
                    self.create_woman(5)
                    self.create_soldier(4)
                    self.create_enemy_tank(2)
                elif self.idle_timer == 30*SECOND:
                    self.create_man(4)
                    self.create_woman(8)
                    self.create_soldier(4)
                    self.create_enemy_tank(2)
                elif self.idle_timer == 33*SECOND:
                    self.create_woman(7)
                    self.create_soldier(6)
                    self.create_enemy_tank(2)
                    self.next_wave_ready = True

            elif self.wave == 6:
                # 40 Men 40 Women 40 Soldiers 25 Tanks
                if self.idle_timer == 2*SECOND:
                    self.create_man(4)
                    self.create_woman(4)
                elif self.idle_timer == 5*SECOND:
                    self.create_soldier(8)
                    self.create_enemy_tank(4)
                elif self.idle_timer == 7*SECOND:
                    self.create_man(4)
                    self.create_woman(4)
                elif self.idle_timer == 12*SECOND:
                    self.create_man(4)
                    self.create_woman(4)
                elif self.idle_timer == 16*SECOND:
                    self.create_soldier(8)
                    self.create_enemy_tank(6)
                elif self.idle_timer == 17*SECOND:
                    self.create_man(4)
                    self.create_woman(4)
                elif self.idle_timer == 22*SECOND:
                    self.create_man(4)  # 25
                    self.create_woman(4)
                elif self.idle_timer == 27*SECOND:
                    self.create_man(4)
                    self.create_woman(4)
                elif self.idle_timer == 30*SECOND:
                    self.create_soldier(8)
                    self.create_enemy_tank(5)
                elif self.idle_timer == 32*SECOND:
                    self.create_man(4)
                    self.create_woman(4)
                elif self.idle_timer == 37*SECOND:
                    self.create_man(4)
                    self.create_woman(4)
                elif self.idle_timer == 38*SECOND:
                    self.create_soldier(6)
                    self.create_enemy_tank(3)
                elif self.idle_timer == 42*SECOND:
                    self.create_man(4)
                    self.create_woman(4)
                elif self.idle_timer == 47*SECOND:
                    self.create_man(4)
                    self.create_woman(4)
                elif self.idle_timer == 50*SECOND:
                    self.create_soldier(10)
                    self.create_enemy_tank(7)
                    self.next_wave_ready = True

            elif self.wave == 7:
                # 60 Men 30 Women 60 Soldiers 30 Tanks 1 MassiveTank
                if self.idle_timer == 4*SECOND:
                    self.create_man(20)
                elif self.idle_timer == 6*SECOND:
                    self.create_soldier(15)
                    self.create_enemy_tank(5)
                elif self.idle_timer == 10*SECOND:
                    self.create_man(10)
                    self.create_woman(8)
                elif self.idle_timer == 15*SECOND:
                    self.create_soldier(10)
                    self.create_enemy_tank(8)
                elif self.idle_timer == 17*SECOND:
                    self.create_man(10)
                    self.create_woman(2)
                elif self.idle_timer == 18*SECOND:
                    self.create_woman(2)
                elif self.idle_timer == 19*SECOND:
                    self.create_woman(2)
                    self.create_soldier(4)
                elif self.idle_timer == 20*SECOND:
                    self.create_woman(2)
                    self.create_soldier(6)
                    self.create_enemy_tank(3)
                elif self.idle_timer == 25*SECOND:
                    self.create_man(15)
                    self.create_woman(10)
                    self.create_soldier(5)
                    self.create_enemy_tank(4)
                elif self.idle_timer == 30*SECOND:
                    self.create_man(5)
                    self.create_woman(4)
                    self.create_soldier(5)
                elif self.idle_timer == 33*SECOND:
                    self.create_soldier(5)
                    self.create_enemy_tank(5)
                elif self.idle_timer == 37*SECOND:
                    self.create_massive_tank()
                elif self.idle_timer == 40*SECOND:
                    self.create_enemy_tank(5)
                    self.next_wave_ready = True

            elif self.wave == 8:
                # 100 Women 50 Soldiers 25 Tanks 5 MassiveTanks
                if self.idle_timer == 2*SECOND:
                    self.create_woman(5)
                    self.create_soldier(3)
                    self.create_enemy_tank()
                    self.create_massive_tank()
                elif self.idle_timer == 4*SECOND:
                    self.create_woman(5)
                    self.create_soldier(7)
                elif self.idle_timer == 8*SECOND:
                    self.create_woman(10)
                    self.create_soldier(5)
                    self.create_enemy_tank(9)
                elif self.idle_timer == 12*SECOND:
                    self.create_woman(5)
                    self.create_soldier(5)
                    self.create_massive_tank()
                elif self.idle_timer == 16*SECOND:
                    self.create_woman(10)
                    self.create_enemy_tank(4)
                elif self.idle_timer == 19*SECOND:
                    self.create_woman(15)
                    self.create_soldier(5)
                elif self.idle_timer == 22*SECOND:
                    self.create_enemy_tank(4)
                    self.create_massive_tank()
                elif self.idle_timer == 24*SECOND:
                    self.create_woman(10)
                    self.create_soldier(4)
                    self.create_enemy_tank(2)
                elif self.idle_timer == 28*SECOND:
                    self.create_woman(10)
                    self.create_soldier(6)
                    self.create_enemy_tank()
                elif self.idle_timer == 32*SECOND:
                    self.create_woman(15)
                elif self.idle_timer == 36*SECOND:
                    self.create_woman(15)
                    self.create_soldier(5)
                elif self.idle_timer == 45*SECOND:
                    self.create_soldier(10)
                    self.create_enemy_tank(4)
                    self.create_massive_tank(2)
                    self.next_wave_ready = True

            elif self.wave == 9:
                # 60 Soldiers 30 Tanks 10 MassiveTanks
                if 1 < self.idle_timer <= 60*SECOND:
                    if self.idle_timer % SECOND == 0:
                        self.create_soldier()
                    if self.idle_timer % (2 * SECOND) == 0:
                        self.create_enemy_tank()
                    if self.idle_timer % (6 * SECOND) == 0:
                        self.create_massive_tank()
                elif self.idle_timer == (60*SECOND)+1:
                    self.next_wave_ready = True

            elif self.wave == 10:
                # 25 Men 40 Women 75 Soldiers 50 Tanks 20 MassiveTanks
                if 1 < self.idle_timer <= 75 * SECOND:
                    if self.idle_timer % SECOND == 0:
                        self.create_soldier()
                    if self.idle_timer % (3*SECOND) == 0:
                        self.create_man()

                if 1 < self.idle_timer <= 100 * SECOND:
                    if self.idle_timer % (5*SECOND) == 0:
                        self.create_woman(2)
                    if self.idle_timer % (20*SECOND) == 0:
                        self.create_massive_tank()
                    if self.idle_timer % (2*SECOND) == 0:
                        self.create_enemy_tank()

                elif self.idle_timer == (100*SECOND)+1:
                    self.next_wave_ready = True

        # If all players are dead, swap to game over screen.
        if len(self.player_list) == 0:
            self.game_over = True

        for enemy in self.enemy_list:
            # Detect if the enemy goes past the left border of the screen, the game is over.
            if enemy.right < 0:
                enemy.kill()
                self.game_over = True

            # Have enemies shoot at a random chance
            if random.randrange(enemy.attack_cooldown) == 0:
                try:
                    target = random.choice(self.player_list)
                    bullet = enemy.attack(target)
                    # If it is a missile, append to missile list to separate from normal indestructible bullet.
                    try:
                        if bullet.guid == "Missile":
                            self.missile_list.append(bullet)

                        self.enemy_bullet_list.append(bullet)
                        self.all_sprites_list.append(bullet)
                    except AttributeError:
                        pass

                except IndexError:  # If no player found, it will swap to game over screen.
                    self.game_over = True

        if not self.game_over:
            # Player movement
            self.player_sprite.move(self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed)
            self.player_sprite2.move(self.up_pressed2, self.down_pressed2, self.left_pressed2, self.right_pressed2)

            self.all_sprites_list.update()
            self.hud_list.update()

            # Updating HUD
            if self.player_sprite.skill_point > 0:
                # Updating HUD when a skill point is available
                if self.p1_hp_HUD_display.current_level % 2 == 0:
                    self.p1_hp_HUD_display.prompt_upgrade()
                if self.p1_dmg_HUD_display.current_level % 2 == 0:
                    self.p1_dmg_HUD_display.prompt_upgrade()
                if self.p1_speed_HUD_display.current_level % 2 == 0:
                    self.p1_speed_HUD_display.prompt_upgrade()
                if self.p1_rotate_HUD_display.current_level % 2 == 0:
                    self.p1_rotate_HUD_display.prompt_upgrade()
                if self.p1_bullet_HUD_display.current_level % 2 == 0:
                    self.p1_bullet_HUD_display.prompt_upgrade()

            elif self.player_sprite.skill_point == 0:
                # Update HUD when there are no skill points available
                if self.p1_hp_HUD_display.current_level % 2 != 0:
                    self.p1_hp_HUD_display.lock_upgrade()
                if self.p1_dmg_HUD_display.current_level % 2 != 0:
                    self.p1_dmg_HUD_display.lock_upgrade()
                if self.p1_speed_HUD_display.current_level % 2 != 0:
                    self.p1_speed_HUD_display.lock_upgrade()
                if self.p1_rotate_HUD_display.current_level % 2 != 0:
                    self.p1_rotate_HUD_display.lock_upgrade()
                if self.p1_bullet_HUD_display.current_level % 2 != 0:
                    self.p1_bullet_HUD_display.lock_upgrade()

            if self.player_sprite2.skill_point > 0:
                # Updating HUD when a skill point is available
                if self.p2_hp_HUD_display.current_level % 2 == 0:
                    self.p2_hp_HUD_display.prompt_upgrade()
                if self.p2_dmg_HUD_display.current_level % 2 == 0:
                    self.p2_dmg_HUD_display.prompt_upgrade()
                if self.p2_speed_HUD_display.current_level % 2 == 0:
                    self.p2_speed_HUD_display.prompt_upgrade()
                if self.p2_rotate_HUD_display.current_level % 2 == 0:
                    self.p2_rotate_HUD_display.prompt_upgrade()
                if self.p2_bullet_HUD_display.current_level % 2 == 0:
                    self.p2_bullet_HUD_display.prompt_upgrade()

            elif self.player_sprite2.skill_point == 0:
                # Update HUD when there are no skill points available
                if self.p2_hp_HUD_display.current_level % 2 != 0:
                    self.p2_hp_HUD_display.lock_upgrade()
                if self.p2_dmg_HUD_display.current_level % 2 != 0:
                    self.p2_dmg_HUD_display.lock_upgrade()
                if self.p2_speed_HUD_display.current_level % 2 != 0:
                    self.p2_speed_HUD_display.lock_upgrade()
                if self.p2_rotate_HUD_display.current_level % 2 != 0:
                    self.p2_rotate_HUD_display.lock_upgrade()
                if self.p2_bullet_HUD_display.current_level % 2 != 0:
                    self.p2_bullet_HUD_display.lock_upgrade()

            # Check for collision between player's bullets and missiles
            for bullet in self.bullet_list:
                missiles = arcade.check_for_collision_with_list(bullet, self.missile_list)

                if len(missiles) > 0:
                    bullet.kill()
                    explosion = Explosion(self.explosion_texture_list, bullet)
                    self.all_sprites_list.append(explosion)
                    for missile in missiles:
                        missile.kill()

            # Check for collision between enemies and players sprites
            for enemy in self.enemy_list:
                players = arcade.check_for_collision_with_list(enemy, self.player_list)

                if len(players) > 0:
                    enemy.kill()
                    explosion = Explosion(self.explosion_texture_list, enemy)
                    self.all_sprites_list.append(explosion)
                    for player in players:
                        player.take_damage(enemy.collision_damage)

            # Check for collision between enemies' bullets and players
            for bullet in self.enemy_bullet_list:
                players = arcade.check_for_collision_with_list(bullet, self.player_list)

                if len(players) > 0:
                    bullet.kill()
                    explosion = Explosion(self.smoke_texture_list, bullet)
                    self.all_sprites_list.append(explosion)
                    for player in players:
                        player.take_damage(bullet.damage)

            # Check for collision between bullets and enemies
            for bullet in self.bullet_list:
                enemies = arcade.check_for_collision_with_list(bullet, self.enemy_list)

                if len(enemies) > 0:
                    bullet.kill()
                    explosion = Explosion(self.explosion_texture_list, bullet)
                    self.all_sprites_list.append(explosion)
                    for enemy in enemies:
                        enemy.take_damage(bullet.damage)

        else:
            game_over_view = GameOverView()
            game_over_view.setup()
            self.window.show_view(game_over_view)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None

    def setup(self):
        self.background = arcade.load_texture("assets/screens/gameOver.png")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        arcade.play_sound(sound_click_button)
        menu_view = MenuView()
        menu_view.setup()
        self.window.show_view(menu_view)


class WinView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None

    def setup(self):
        self.background = arcade.load_texture("assets/screens/winScreen.png")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        arcade.play_sound(sound_click_button)
        menu_view = MenuView()
        menu_view.setup()
        self.window.show_view(menu_view)


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view
        self.pause_screen = arcade.Sprite("assets/screens/pause.png")
        self.pause_screen.center_x = SCREEN_WIDTH / 2
        self.pause_screen.center_y = SCREEN_HEIGHT / 2

    def on_draw(self):
        arcade.start_render()

        background = self.game_view.background_list
        decor = self.game_view.decor_list
        all_sprite = self.game_view.all_sprites_list
        background.draw()
        decor.draw()
        all_sprite.draw()

        self.pause_screen.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.P:
            self.window.show_view(self.game_view)
        elif key == arcade.key.ESCAPE:
            menu_view = MenuView()
            menu_view.setup()
            self.window.show_view(menu_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    menu_view.setup()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
