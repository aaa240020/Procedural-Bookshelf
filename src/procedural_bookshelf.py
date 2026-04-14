import maya.cmds as cmds
import random


class Bookshelf():

    overall_height = 2  # overall height is the height of the shelf without the legs

    shelf_height = overall_height - (overall_height / 62.5)
    shelf_width = 1
    shelf_depth = 0.3
    shelf_levels = 6

    shelf_dividers_height = overall_height / 125  # the width and depth of the dividers are the same as the entire shelf
    shelf_dividers_width = shelf_width - (shelf_dividers_height * 2)

    books_offset = 0  # a slider will be added to adjust
    books_height = (shelf_height / shelf_levels) - shelf_dividers_height  # a slider will be added to adjust
    books_depth = shelf_depth - (shelf_depth / 10)  # a slider will be added to adjust

    shelf_leg_height = overall_height * (1/25)

    def generate_dividers(self):
        dividers = []
        for level in range(1, self.shelf_levels):
            divider = cmds.polyCube(height=self.shelf_dividers_height,
                                    width=self.shelf_dividers_width,
                                    depth=self.shelf_depth,
                                    name="divider_plank_1")[0]
            cmds.xform(divider,
                       translation=[0,
                                    ((self.shelf_height/2) +
                                     (self.shelf_dividers_height/2)) -
                                    (((self.shelf_height +
                                       self.shelf_dividers_height) /
                                     self.shelf_levels) * level),
                                    0])
            self._freeze_transforms(divider)
            dividers.append(divider)

        grp_name = cmds.group(dividers, name="Dividers")
        return grp_name

    def generate_legs(self):
        legs = []
        for x_axis_duplicates in [-1, 1]:
            for z_axis_dupllicates in [-1, 1]:
                leg = cmds.polyCylinder(height=self.shelf_leg_height,
                                        radius=self.shelf_leg_height/2.5,
                                        name="shelf_leg_1")[0]
                cmds.xform(leg,
                           translation=[(((self.shelf_width/2) -
                                        (self.shelf_dividers_height * 4)) *
                                        x_axis_duplicates),
                                        (-self.overall_height/2) -
                                        self.shelf_leg_height/2,
                                        (((self.shelf_depth/2) -
                                         (self.shelf_dividers_height * 4)) *
                                        z_axis_dupllicates),])
                self._freeze_transforms(leg)
                legs.append(leg)

        grp_name = cmds.group(legs, name="Shelf_Legs")
        return grp_name

    def generate_frame(self):
        frame = []
        for duplicates in range(-1, 2, 2):
            vertical_plank = cmds.polyCube(height=self.shelf_height,
                                           width=self.shelf_dividers_height,
                                           depth=self.shelf_depth,
                                           name="vertical_plank_1")[0]
            cmds.xform(vertical_plank,
                       translation=[((self.shelf_width/2) -
                                    self.shelf_dividers_height/2) *
                                    duplicates,
                                    0, 0])
            self._freeze_transforms(vertical_plank)
            frame.append(vertical_plank)
            horizontal_plank = cmds.polyCube(height=self.shelf_dividers_height,
                                             width=self.shelf_width,
                                             depth=self.shelf_depth,
                                             name="horizontal_plank_1")[0]
            cmds.xform(horizontal_plank,
                       translation=[0,
                                    ((self.shelf_height/2) +
                                     self.shelf_dividers_height/2) *
                                    duplicates,
                                    0])
            self._freeze_transforms(horizontal_plank)
            frame.append(horizontal_plank)

        back_plank = cmds.polyCube(height=self.overall_height,
                                   width=self.shelf_width,
                                   depth=self.shelf_dividers_height,
                                   name="back_plank")[0]
        cmds.xform(back_plank,
                   translation=[0,
                                0,
                                -(self.shelf_depth/2) -
                                (self.shelf_dividers_height/2)])
        self._freeze_transforms(back_plank)
        frame.append(back_plank)

        frame.append(self.generate_dividers())
        frame.append(self.generate_legs())
        grp_name = cmds.group(frame, name="Bookshelf_Frame")
        return grp_name

    def generate_books(self):
        pile_of_books = []

        book_x_axis = -(self.shelf_dividers_width/2) + self.books_offset

        while book_x_axis < (self.shelf_dividers_width/2):
            random_width = random.uniform(self.overall_height/100,
                                          self.overall_height/40)
            random_height = random.uniform(self.books_height/1.83529,
                                           self.books_height)
            random_depth = random.uniform(self.books_depth/2.16,
                                          self.books_depth)

            if book_x_axis + random_width > (self.shelf_dividers_width/2):
                break

            book = cmds.polyCube(height=random_height,
                                 width=random_width,
                                 depth=random_depth,
                                 name="book_1")[0]
            cmds.xform(book, pivots=[-random_width/2,
                                     -random_height/2,
                                     0])
            cmds.xform(book,
                       translation=[book_x_axis + random_width,
                                    random_height/2,
                                    (-self.books_depth/2) +
                                    (random_depth/2),])
            book_x_axis += random_width
            self._freeze_transforms(book)
            #  self._join_geometry(book)
            pile_of_books.append(book)

        grp_name = cmds.group(pile_of_books, name="Book_Stack_1")
        return grp_name

    def generate_stacks_of_books(self):
        books = []

        for book_stack in range(1, self.shelf_levels + 1):
            sub_grp_name = self.generate_books()
            cmds.xform(sub_grp_name,
                       translation=[0,
                                    ((self.shelf_height/2) +
                                     (self.shelf_dividers_height/2)) -
                                    (((self.shelf_height +
                                       self.shelf_dividers_height) /
                                     self.shelf_levels) * book_stack),
                                    0])
            self._freeze_transforms(sub_grp_name)
            books.append(sub_grp_name)

        grp_name = cmds.group(books, name=("Books"))
        return grp_name

    def generate_bookshelf(self):
        book_shelf = []

        book_shelf.append(self.generate_frame())
        book_shelf.append(self.generate_stacks_of_books())

        grp_name = cmds.group(book_shelf, name="Bookshelf")
        return grp_name

    def _freeze_transforms(self, name):
        cmds.makeIdentity(name, apply=True, translate=True, rotate=True,
                          scale=True, normal=False, preserveNormals=True)
