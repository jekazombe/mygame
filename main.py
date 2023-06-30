import arcade
import random
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750
SCREEN_TITLE = "Jump Chel"
SCALING = 0.2
counter = 0
counter_speed = -1
count = 100

new_game = False
game_over = False
text = False

class JumpChel(arcade.Window):

    def remove_sprite(self):
        for i in self.all_sprite:
            if round(i.bottom) == 0:
                i.remove_from_sprite_lists()

    def add_oblako(self):
        self.oblaka_sprite = arcade.Sprite("image/oblako.png", SCALING / 1.5)
        self.oblaka_sprite.bottom = random.randint(self.height, self.height + 80)
        self.oblaka_sprite.right = random.randint(10, self.width - 10)

        self.oblaka_list.append(self.oblaka_sprite)
        self.all_sprite.append(self.oblaka_sprite)

    def add_rect(self):
        b = 800
        self.rect_sprite = arcade.Sprite("image/rect.png", SCALING / 3)
        self.rect_sprite.bottom = random.randint(b, b + 100)
        self.rect_sprite.right = random.randint(10, self.width - 10)

        self.rect_list.append(self.rect_sprite)
        self.all_sprite.append(self.rect_sprite)

    def add_rect_nul(self):
        a = 100
        for i in range(0, 6):
            self.rect_sprite_nul = arcade.Sprite("image/rect.png", SCALING / 3)
            self.rect_sprite_nul.bottom = random.randint(a, a + 100)
            self.rect_sprite_nul.right = random.randint(10, self.width - 10)
            a += 100

            self.rect_nul_list.append(self.rect_sprite_nul)
            self.all_sprite.append(self.rect_sprite_nul)

    def jumpchel_height_up(self):
        arcade.play_sound(self.jump_sound, 1)
        global counter
        self.player_sprite.change_y = 80
        counter += 1

    def jumpchel_height_down(self):
        global counter_speed
        self.player_sprite.change_y = counter_speed

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_list = arcade.SpriteList()
        self.rect_nul_list = arcade.SpriteList()
        self.oblaka_list = arcade.SpriteList()
        self.rect_list = arcade.SpriteList()
        self.all_sprite = arcade.SpriteList()

        self.background_music = arcade.load_sound("sound/tgfcoder-FrozenJam-SeamlessLoop.mp3")
        self.media_player = self.background_music.play()
        self.jump_sound = arcade.load_sound("sound/pew.wav")
        self.jump_down_sound = arcade.load_sound("sound/expl6.wav")
        self.game_over_sound = arcade.load_sound("sound/game_over.mp3")

        arcade.set_background_color(arcade.color.BLUE)

    def setup(self):

        self.media_player.play()
        self.media_player.volume = 0.2

        self.player_sprite = arcade.Sprite("image/stick_men1.png", SCALING / 1.4)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.bottom = 3

        self.player_list.append(self.player_sprite)
        self.all_sprite.append(self.player_sprite)

        self.add_rect_nul()
        arcade.set_background_color(arcade.color.BLUE)

    def on_draw(self):
        global new_game, game_over, counter, text
        arcade.start_render()
        self.player_list.draw()
        self.oblaka_list.draw()
        self.rect_list.draw()
        self.rect_nul_list.draw()
        self.all_sprite.draw()

        if new_game == False:
            arcade.draw_text("Нажмите SPACE чтобы начать игру", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.RED, 30, anchor_x="center")
            text = True
        if text == True:
            arcade.draw_text(f"Счет: {counter}", 700, 700, arcade.color.WHITE, 15, anchor_x="center")

        if round(self.player_sprite.bottom) == 0:
            self.media_player1 = self.jump_down_sound.play()
            self.media_player2 = self.game_over_sound.play()
            arcade.draw_text("GAME OVER", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.RED, 30, anchor_x="center")

    def on_update(self, delta_time: float):
        global new_game, counter, counter_speed, count, text
        sec = 0
        self.remove_sprite()
        if counter == count:
            counter_speed -= 2
            count += 100
        if new_game:
            if round(self.player_sprite.bottom) == 0:
                text = False
                self.media_player.pause()
                for i in self.all_sprite:
                    i.remove_from_sprite_lists()
                while sec != 3:
                    time.sleep(1)
                    sec += 1
                else:
                    arcade.close_window()
            elif round(self.player_sprite.bottom) == 3:
                arcade.play_sound(self.jump_sound, 1)
                self.jumpchel_height_up()
            elif round(self.player_sprite.bottom) == 200:
                self.jumpchel_height_down()
            elif self.player_sprite.collides_with_list(self.rect_nul_list) or self.player_sprite.collides_with_list(self.rect_list):
                arcade.play_sound(self.jump_sound, 1)
                self.add_oblako()
                self.add_rect()
                self.jumpchel_height_up()

                for i in self.rect_nul_list:
                    i.change_y = -100
                for i in self.rect_list:
                    i.change_y = -100
                for i in self.oblaka_list:
                    i.change_y = -100
            else:
                self.jumpchel_height_down()
                for i in self.rect_nul_list:
                    i.change_y = 1
                for i in self.rect_list:
                    i.change_y = 1
                for i in self.oblaka_list:
                    i.change_y = 1

        self.player_list.update()
        self.oblaka_list.update()
        self.rect_list.update()
        self.rect_nul_list.update()

        for sprite in self.player_list:
            sprite.center_x = int(sprite.center_x + sprite.change_x * delta_time)
            sprite.center_y = int(sprite.center_y + sprite.change_y * delta_time)
        for sprite in self.rect_list:
            sprite.center_x = int(sprite.center_x + sprite.change_x * delta_time)
            sprite.center_y = int(sprite.center_y + sprite.change_y * delta_time)
        for sprite in self.oblaka_list:
            sprite.center_x = int(sprite.center_x + sprite.change_x * delta_time)
            sprite.center_y = int(sprite.center_y + sprite.change_y * delta_time)

        if self.player_sprite.top > self.height:
            self.player_sprite.top = self.height
        if self.player_sprite.right > self.width:
            self.player_sprite.right = self.width
        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0

    def on_key_press(self, symbol: int, modifiers: int):
        global new_game
        if symbol == arcade.key.SPACE:
            new_game = True
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_x = -10
        if symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = 10

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.LEFT:
            self.player_sprite.change_x = 0
        if symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

def main():
    """ Main function """
    window = JumpChel()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()