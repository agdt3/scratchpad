import math

from enum import Enum
from pygame import (
    draw,
    sprite,
    mask,
    Surface,
)


class SelectType(Enum):
    FACE = 'face'
    BORDER = 'border'


class HexTiles(sprite.Group):
    def __init__(
        self,
        size=(100, 100),
        rows=1,
        columns=1,
        spacing=0,
        color=(0, 0, 255),
        select_color=(100, 100, 255),
        select_type=SelectType.FACE,
        area=None
    ):
        sprite.Group.__init__(self)

        self.size = size
        self.rows = rows
        self.columns = columns
        self.spacing = spacing
        self.color = color
        self.select_color = select_color
        self.select_type = select_type

        self.adj = 0

        # area overrides size and begins tiling
        # based on number of rows and columns
        self.area = area
        if self.area is not None:
            self.calculate_size()

        self.points = self.generate_points()
        self.generate_tiles()

    def calculate_size(self):
        width = self.area[0]
        height = self.area[1]

        if self.columns > 1:
            rows = self.rows + 0.5
        else:
            rows = self.rows

        hex_height = (height - (self.rows * self.spacing)) / rows

        opp = hex_height / 2
        self.adj = opp / math.tan(math.radians(60))
        #hex_width = (width + (adj * self.columns)) / self.columns
        hex_width = (width / self.columns) + self.adj

        self.size = (hex_width, hex_height)

    def generate_points(self):
        width, height = self.size

        quarter_width = width / 4
        a = (0, height / 2)
        b = (self.adj, 0)
        c = (width - self.adj, 0)
        #b = (quarter_width, 0)
        #c = (3 * quarter_width, 0)
        d = (width, height / 2)
        e = (width - self.adj, height)
        f = (self.adj, height)
        #e = (3 * quarter_width, height)
        #f = (quarter_width, height)

        return [a, b, c, d, e, f]

    def generate_tiles(self):
        width, height = self.size
        for row in range(self.rows):
            for col in range(self.columns):
                offset_x = col * (width - self.adj + self.spacing)
                #offset_x = col * ((3 * width / 4) + self.spacing)
                if col % 2 == 0:
                    offset_y = row * (height + self.spacing)
                else:
                    offset_y = row * (height + self.spacing) + (height / 2)
                offset = (math.floor(offset_x), math.floor(offset_y))
                self.add(
                    HexTile(
                        points=self.points,
                        position=offset,
                        size=self.size,
                        color=self.color,
                        select_color=self.select_color,
                        select_type=self.select_type
                    )
                )

    def check_colissions(self, pos):
        for sprite in self.sprites():
            if sprite.rect.collidepoint(pos):
                if sprite.is_pos_in_mask(pos):
                    self.deselect_all()
                    sprite.select_toggle()

    def deselect_all(self):
        for sprite in self.sprites():
            sprite.select_toggle(selected=False)


class HexTile(sprite.Sprite):
    def __init__(
        self,
        points=None,
        size=None,
        position=None,
        color=None,
        select_color=None,
        select_type=SelectType.FACE
    ):
        sprite.Sprite.__init__(self)

        self.points = points
        self.size = size
        self.position = position
        self.color = color
        self.selected_color = select_color
        self.select_type = select_type

        self.image = Surface(self.size)  # exposed image
        self.unselected_image = Surface(self.size)  # base image
        self.selected_image = Surface(self.size)  # base selected image

        self.generate_image(self.unselected_image, self.color, self.points)
        self.generate_image(self.selected_image, self.selected_color, self.points)

        # Draw unselected image onto current image
        self.image.blit(self.unselected_image, (0, 0))

        # Move image
        self.rect = self.image.get_rect(topleft=self.position)

        self.selected = False

        # mask sets all colorkey pixels to 0 for if colorkey is set
        # Note that mask never moves, so requires offset calculations
        # it is also possible for a group of tiles to share one mask
        self.mask = mask.from_surface(self.image)

    def update(self):
        pass

    def generate_image(self, surface, color, points):
        # Make all black pixels transparent when being drawn onto screen
        self.image.set_colorkey((0,0,0))
        self.draw_polygon(surface, color, points)

    def is_pos_in_mask(self, pos):
        offset_pos = (pos[0] - self.position[0], pos[1] - self.position[1])
        try:
            if self.mask.get_at(offset_pos):
                return True
            else:
                return False
        except IndexError:
            return False

    def draw_polygon(self, surface, color, points):
        # Draw polygon
        draw.polygon(surface, color, points, 0)

    def select_toggle(self, selected=None):
        if selected is None:
            self.selected = not self.selected
        else:
            self.selected = selected
        # A different version of this would be to alter the pixel values
        # directly via surfarray
        # Note: mask doesn't need to get refreshed since the image shape,
        # position and orientation are the same
        if self.selected:
            if self.select_type is SelectType.FACE:
                self.image.blit(self.selected_image, self.selected_image.get_rect())
            else:
                # This is imperfect
                draw.polygon(self.image, self.selected_color, self.points, 3)
        else:
            self.image.blit(self.unselected_image, self.unselected_image.get_rect())
