import pyglet
import random


class Bunny(pyglet.sprite.Sprite):
    gravity = 0.75
    bounce = 0.85

    def __init__(self, image, x, y, batch):
        super().__init__(image, x, y, batch=batch)

        self.real_x = x
        self.real_y = y
        self.speed_x = random.random() * 10
        self.speed_y = -random.random() * 10 + 5

    def update(self, window_width, window_height):
        # self.x and self.y are properties, very expensive to change.
        self.real_x += self.speed_x
        self.real_y += self.speed_y

        self.speed_y -= self.gravity

        if self.real_x < 0:
            self.real_x = 0
            self.speed_x = -self.speed_x
        elif self.real_x > window_width:
            self.real_x = window_width
            self.speed_x = -self.speed_x

        if self.real_y < 0:
            self.real_y = 0
            self.speed_y *= -self.bounce

            if random.random() < 0.5:
                self.speed_y += random.random() * 6
        elif self.real_y > window_height:
            self.real_y = window_height
            self.speed_y = 0

        self.x = int(self.real_x)
        self.y = int(self.real_y)


class App(pyglet.window.Window):
    def __init__(self):
        super().__init__(800, 600, "Python bunnymark", resizable=True)

        #self.image.

        self.image = pyglet.image.load('bunny.png')
        self.image.anchor_x = self.image.width // 2
        self.image.anchor_y = self.image.height // 2

        self.batch = pyglet.graphics.Batch()

        self.bunnies = []

        self.is_mouse_pressed = False

        @self.event
        def on_mouse_press(*_):
            self.is_mouse_pressed = True

        @self.event
        def on_mouse_release(*_):
            self.is_mouse_pressed = False

        self.statistics_label = pyglet.text.Label(self.get_statistics())

        pyglet.clock.schedule_interval(self.update, .01)

        pyglet.app.run()

    def get_statistics(self):
        return f"FPS: {round(pyglet.clock.get_fps(), 1)}\n" \
               f"Bunnies: {len(self.bunnies)}"

    def spawn_bunny(self):
        self.bunnies.append(Bunny(self.image, 0.0, self.height, self.batch))

    def update(self, dt):
        if self.is_mouse_pressed:
            for i in range(50):
                self.spawn_bunny()

        for bunny in self.bunnies:
            bunny.update(self.width, self.height)

        self.statistics_label.text = self.get_statistics()

    def on_draw(self):
        self.clear()
        self.batch.draw()
        self.statistics_label.draw()


if __name__ == '__main__':
    app = App()
