import arcade
import math
import random

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "ThaiTank BattleGrounds"
SECOND = 60

ENEMY_SPAWN_MARGIN = 64
ENEMY_SPAWN_X = ENEMY_SPAWN_MARGIN + SCREEN_WIDTH

PLAY_ZONE_LIMIT_BOTTOM = 128
PLAY_ZONE_LIMIT_TOP = SCREEN_HEIGHT - PLAY_ZONE_LIMIT_BOTTOM

TILE_SCALING = 1

EXPLOSION_TEXTURES = 5

# Sound
sound_hit = arcade.load_sound("assets/sounds/bookClose.ogg")
sound_tank_shoot = arcade.load_sound("assets/sounds/laser1.ogg")
sound_missile_shoot = arcade.load_sound("assets/sounds/laser2.ogg")
sound_gun_shoot = arcade.load_sound("assets/sounds/laser3.ogg")
sound_upgrade = arcade.load_sound("assets/sounds/zap1.ogg")
sound_click_button = arcade.load_sound("assets/sounds/switch8.ogg")


class TurningSprite(arcade.Sprite):
    """ Sprite that sets its angle to the direction it is traveling in. """
    def update(self):
        super().update()
        self.angle = math.degrees(math.atan2(self.change_y, self.change_x)) - 90


class Tank(arcade.Sprite):
    """ Class that represent a tank for each player. """
    def __init__(self, position, filename: str, scale: float = 1):
        super().__init__(filename, scale)

        # Upgradable attributes
        self.health = 100
        self.max_health = 100
        self.max_speed = 0
        self.max_rotate_speed = 0
        self.damage = 0
        self.bullet_speed = 0
        self.skill_point = 0

        # Skill levels
        self.hp_lvl = 0
        self.speed_lvl = 0
        self.dmg_lvl = 0
        self.bullet_speed_lvl = 0
        self.rotate_speed_lvl = 0

        # Normal attributes
        self.set_hp()
        self.set_damage()
        self.set_speed()
        self.set_bullet_speed()
        self.set_rotate_speed()
        self.ammo = 30
        self.reloading = False
        self.reload_time = 0
        self.reload_timer = 0
        self.angle = 180
        self.speed = 0
        self.center_x = position[0]
        self.center_y = position[1]
        self.ammo_x = self.center_x
        self.ammo_y = self.center_y + self.width

    def reload(self):
        self.ammo = 0
        self.reloading = True

    def reloaded(self):
        self.ammo = 30
        self.reload_time = 0
        self.reload_timer = 0
        self.reloading = False

    def respawn(self, hp, dmg, speed, rot_speed, bul_speed):
        """ A function to calibrate player's upgrades upon respawning. """
        self.hp_lvl = hp
        self.dmg_lvl = dmg
        self.speed_lvl = speed
        self.rotate_speed_lvl = rot_speed
        self.bullet_speed_lvl = bul_speed

        self.set_hp()
        self.set_damage()
        self.set_bullet_speed()
        self.set_rotate_speed()
        self.set_speed()

    def set_hp(self):
        """ Setting player's health according to the upgrade level. """
        if self.hp_lvl == 0:
            self.max_health = 100
        elif self.hp_lvl == 1:
            self.max_health = 150
        elif self.hp_lvl == 2:
            self.max_health = 200
        elif self.hp_lvl == 3:
            self.max_health = 250
        elif self.hp_lvl == 4:
            self.max_health = 300
        self.health = self.max_health

    def upgrade_hp(self):
        """ Upgrading health point level. """
        self.skill_point -= 1
        self.hp_lvl += 1

        self.set_hp()

    def set_damage(self):
        """ Setting player's damage according to the upgrade level."""
        if self.dmg_lvl == 0:
            self.damage = 5
        elif self.dmg_lvl == 1:
            self.damage = 10
        elif self.dmg_lvl == 2:
            self.damage = 20
        elif self.dmg_lvl == 3:
            self.damage = 30
        elif self.dmg_lvl == 4:
            self.damage = 40

    def upgrade_damage(self):
        """ Upgrading damage level. """
        self.skill_point -= 1
        self.dmg_lvl += 1

        self.set_damage()

    def set_speed(self):
        """ Setting player's speed according to the upgrade level."""
        if self.speed_lvl == 0:
            self.max_speed = 1.5
        elif self.speed_lvl == 1:
            self.max_speed = 2.25
        elif self.speed_lvl == 2:
            self.max_speed = 3
        elif self.speed_lvl == 3:
            self.max_speed = 4

    def upgrade_speed(self):
        """ Upgrading speed level. """
        self.skill_point -= 1
        self.speed_lvl += 1

        self.set_speed()

    def set_rotate_speed(self):
        """ Setting player's rotation speed according to the upgrade level."""
        if self.rotate_speed_lvl == 0:
            self.max_rotate_speed = 2
        elif self.rotate_speed_lvl == 1:
            self.max_rotate_speed = 2.75
        elif self.rotate_speed_lvl == 2:
            self.max_rotate_speed = 3.5
        elif self.rotate_speed_lvl == 3:
            self.max_rotate_speed = 4.5

    def upgrade_rotate_speed(self):
        """ Upgrading rotation speed level. """
        self.skill_point -= 1
        self.rotate_speed_lvl += 1

        self.set_rotate_speed()

    def set_bullet_speed(self):
        """ Setting player's damage according to the upgrade level."""
        if self.bullet_speed_lvl == 0:
            self.bullet_speed = 5.75
        elif self.bullet_speed_lvl == 1:
            self.bullet_speed = 7.5
        elif self.bullet_speed_lvl == 2:
            self.bullet_speed = 9
        elif self.bullet_speed_lvl == 3:
            self.bullet_speed = 11

    def upgrade_bullet_speed(self):
        """ Upgrading damage level. """
        self.skill_point -= 1
        self.bullet_speed_lvl += 1

        self.set_bullet_speed()

    def update(self):
        """ Update the tank """
        # Reload
        if self.ammo == 0:
            self.reload()

        if self.reloading:
            self.reload_time += 1
            self.reload_timer = self.reload_time // 9
            if self.reload_time > 90:
                self.reloaded()

        # Ammo indicator
        self.ammo_x = self.center_x
        self.ammo_y = self.center_y + self.width

        # Calculating speed
        angle_rad = math.radians(self.angle)

        self.angle += self.change_angle

        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)

        # Limiting the play area
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH

        if self.bottom < PLAY_ZONE_LIMIT_BOTTOM:
            self.bottom = PLAY_ZONE_LIMIT_BOTTOM
        elif self.top > PLAY_ZONE_LIMIT_TOP:
            self.top = PLAY_ZONE_LIMIT_TOP

        if self.health <= 0:
            self.kill()

    def shoot(self, bullet: str):
        """ A function to shoot the bullet """
        bullet_sprite = BulletSprite(self, bullet)
        flash_sprite = TankFlash(self)
        arcade.play_sound(sound_tank_shoot)
        self.ammo -= 1

        return bullet_sprite, flash_sprite

    def move(self, up, down, left, right):
        """ A function to move the tank """
        self.speed = 0
        self.change_angle = 0

        if up and not down:
            self.speed = -self.max_speed
        elif down and not up:
            self.speed = self.max_speed

        if left and not right:
            self.change_angle = self.max_rotate_speed
        elif right and not left:
            self.change_angle = -self.max_rotate_speed

    def take_damage(self, damage):
        self.health -= damage


class BulletSprite(TurningSprite):
    """
    Class that represent a bullet.

    Sprite that aligns to its direction.
    """
    def __init__(self, origin: Tank, filename: str, scale: float = 1.5):
        super().__init__(filename, scale)
        self.guid = "Bullet"

        # Calculate the direction of the bullet
        self.change_y = math.cos(math.radians(origin.angle - 180)) * origin.bullet_speed
        self.change_x = -math.sin(math.radians(origin.angle - 180)) * origin.bullet_speed

        self.center_x = origin.center_x
        self.center_y = origin.center_y

        self.damage = origin.damage

    def update(self):
        super().update()
        if self.center_x < 0 or self.center_x > SCREEN_WIDTH or \
           self.center_y > SCREEN_HEIGHT or self.center_y < 0:
            self.kill()


class TankFlash(TurningSprite):
    """ This class creates a flash after shooting. """
    def __init__(self, origin: Tank):
        super().__init__("assets/tanks/shotRed2.png")

        # Calculating the position of the tank barrel and set it to the flash center.
        self.change_x = -math.sin(math.radians(origin.angle - 180)) * 2
        self.change_y = math.cos(math.radians(origin.angle - 180)) * 2
        self.offset_y = self.change_y * origin.height/2
        self.offset_x = self.change_x * origin.width/2

        self.center_x = origin.center_x + self.offset_x
        self.center_y = origin.center_y + self.offset_y
        self.age = 0

    def update(self):
        super().update()
        # Flash lasts for a split second
        self.age += 1
        if self.age > 4:
            self.kill()


class Explosion(arcade.Sprite):
    """ This class creates explosion animation. """
    def __init__(self, texture_list, sprite):
        super().__init__(texture_list[0].name, 0.7)

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list
        self.timer = 0
        arcade.play_sound(sound_hit)

        # Set up the coordinates of the explosion
        self.center_x = sprite.center_x
        self.center_y = sprite.center_y

    def update(self):
        """ Explosion animation """
        # Update to the next frame of animation. If at the end of the list, delete this sprite.
        self.timer += 1

        if self.timer % 3 == 0:
            self.current_texture += 1

        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
            self.scale = 0.7
        else:
            self.kill()


class HUD(arcade.Sprite):
    """ A class for loading HUD. """
    def __init__(self, texture_list, center_x):
        super().__init__(texture_list[0].name, 1)

        # Start at the first level
        self.current_level = 0
        self.textures = texture_list

        self.center_x = center_x
        self.bottom = 0

    def update(self):
        if self.current_level < len(self.textures):
            self.set_texture(self.current_level)

        self.bottom = 0

    def level_up(self):
        self.current_level += 2
        arcade.play_sound(sound_upgrade)

    def prompt_upgrade(self):
        self.current_level += 1

    def lock_upgrade(self):
        self.current_level -= 1

    def next_lvl(self):
        self.current_level += 1


class WaveHUD(arcade.Sprite):
    """ A class for showing wave feedback on the screen."""
    def __init__(self, texture_list, wave=0):
        super().__init__(texture_list[wave].name)

        self.center_x = SCREEN_WIDTH / 2
        self.top = SCREEN_HEIGHT - 236.5
        self.age = 0

    def update(self):
        super().update()

        self.age += 1
        if self.age > 180:
            self.kill()


class TankHUD(arcade.Sprite):
    """ A class for representing player HUD """
    def __init__(self, filename, center_x):
        super().__init__(filename)
        self.center_y = 64
        self.center_x = center_x
        self.angle = 180


class Enemy(arcade.Sprite):
    """ Parent class for all Enemy types. All functions of enemies will be in this class."""
    def __init__(self, filename: str, scale: float = 1):
        super().__init__(filename, scale)
        self.angle = 180
        self.center_x = ENEMY_SPAWN_X + 120 * random.random()
        self.center_y = random.randint(PLAY_ZONE_LIMIT_BOTTOM, PLAY_ZONE_LIMIT_TOP)
        self.speed = 1
        self.health = 0  # Dummy HP
        self.attack_cooldown = 0
        self.collision_damage = 0

        # HP Indicator position
        self.hp_x = self.center_x
        self.hp_y = self.center_y + self.height/2 + 10

    def update(self):
        super().update()
        self.center_x -= self.speed
        self.hp_x = self.center_x

        if self.health <= 0:
            self.kill()

    def take_damage(self, damage):
        self.health -= damage

    def attack(self, target):
        raise NotImplementedError()


class Man(Enemy):
    def __init__(self):
        super().__init__("assets/targets/manBlue_stand.png", 0.5)
        self.health = 10
        self.speed += 0.25 * random.random()
        self.collision_damage = 25
        self.attack_cooldown = 100000

    def attack(self, target):
        pass


class Woman(Enemy):
    def __init__(self):
        super().__init__("assets/targets/womanGreen_hold.png", 0.5)
        self.health = 10
        self.speed = 1.75 + 0.3 * random.random()
        self.collision_damage = 20
        self.attack_cooldown = 100000

    def attack(self, target):
        pass


class Soldier(Enemy):
    def __init__(self):
        super().__init__("assets/targets/soldier1_machine.png", 0.5)
        self.health = 20
        self.speed += 0.4 * random.random()
        self.collision_damage = 40
        self.attack_cooldown = 500

    def attack(self, target):
        bullet = EnemyBullet()
        bullet.center_x = self.center_x
        bullet.center_y = self.center_y + 5
        arcade.play_sound(sound_gun_shoot)
        return bullet


class EnemyTank(Enemy):
    def __init__(self):
        super().__init__("assets/tanks/tank_dark.png", 0.75)
        self.health = 75
        self.angle = 270
        self.speed = 0.7 + 0.2 * random.random()
        self.collision_damage = 100
        self.attack_cooldown = 1250

    def attack(self, target):
        start_x = self.center_x
        start_y = self.center_y
        dest_x = target.center_x
        dest_y = target.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y

        angle = math.atan2(y_diff, x_diff)
        self.angle = math.degrees(angle) + 90

        bullet = EnemyTankBullet(self, angle)
        arcade.play_sound(sound_tank_shoot)

        return bullet


class MassiveTank(Enemy):
    def __init__(self):
        super().__init__("assets/tanks/tank_huge.png")
        self.health = 350
        self.angle = 270
        self.speed = 0.4 + 0.2 * random.random()
        self.collision_damage = 300
        self.attack_cooldown = 2500

    def attack(self, target):
        bullet = HomingMissile(self, target)
        arcade.play_sound(sound_missile_shoot)

        return bullet


class EnemyProjectile(TurningSprite):
    """ A parent class for enemies' projectiles. """
    def __init__(self, filename, scale):
        super().__init__(filename, scale)
        self.guid = "Projectile"
        self.speed = 0
        self.damage = 0

    def update(self):
        super().update()

        if self.center_x < 0 or self.center_x > SCREEN_WIDTH or \
           self.center_y > SCREEN_HEIGHT or self.center_y < 0:
            self.kill()

    def follow_sprite(self, target):
        raise NotImplementedError()


class EnemyBullet(EnemyProjectile):
    def __init__(self):
        super().__init__("assets/tanks/bulletBlue3_outline.png", 0.75)
        self.guid = "EnemyBullet"
        self.speed = 2.5
        self.damage = 10
        self.change_x = -self.speed

    def follow_sprite(self, target):
        pass


class EnemyTankBullet(EnemyProjectile):
    def __init__(self, origin, angle):
        super().__init__("assets/tanks/bulletDark2_outline.png", 1)
        self.guid = "EnemyTankBullet"
        self.damage = 25
        self.speed = 3
        self.center_x = origin.center_x
        self.center_y = origin.center_y

        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

    def follow_sprite(self, target):
        pass


class HomingMissile(EnemyProjectile):
    def __init__(self, origin, target):
        super().__init__("assets/tanks/homingMissile.png", 1)
        self.guid = "Missile"
        self.damage = 75
        self.speed = 1
        self.center_x = origin.center_x
        self.center_y = origin.center_y
        self.target = target

    def follow_sprite(self, target):
        self.center_x += self.change_x
        self.center_y += self.change_y

        start_x = self.center_x
        start_y = self.center_y
        dest_x = target.center_x
        dest_y = target.center_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed

    def update(self):
        super().update()

        self.follow_sprite(self.target)

        if self.target.health == 0:
            self.kill()
