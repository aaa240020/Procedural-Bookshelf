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
