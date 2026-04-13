import maya.cmds as cmds


class Bookshelf():

    overall_height = 2  # overall height is the height of the shelf without the legs

    shelf_dividers_height = overall_height / 125  # the width and depth of the dividers are the same as the entire shelf

    shelf_height = overall_height - (overall_height / 62.5)
    shelf_width = 1
    shelf_depth = 0.3
    books_offset = 0  # a slider will be added to adjust
    shelf_levels = 6
    books_height = (shelf_height / shelf_levels) - shelf_dividers_height  # a slider will be added to adjust
    books_depth = shelf_depth - (shelf_depth / 5)  # a slider will be added to adjust

    shelf_leg_height = overall_height / 20

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
        
        back_plank = cmds.polyCube(height=self.overall_height,
                                   width=self.shelf_width,
                                   depth=self.shelf_dividers_height,
                                   name="back_plank")[0]
        cmds.xform(back_plank,
                   translation=[0,
                                0,
                                -(self.shelf_depth/2) -
                                (self.shelf_dividers_height/2)])
        
        frame.append(self.generate_dividers())
        frame.append(self.generate_legs())
        grp_name = cmds.group(frame, name="Bookshelf_Frame")
        return grp_name

    def generate_bookshelf(self):
        self.generate_frame(self)
        self.generate_books()
