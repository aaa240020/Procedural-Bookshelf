import maya.cmds as cmds
import random
import maya.OpenMayaUI as omui
from PySide6 import QtWidgets, QtCore
from shiboken6 import wrapInstance


def get_maya_main_win():
    main_win_addr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win_addr), QtWidgets.QWidget)


class BookshelfWindow(QtWidgets.QDialog):

    def __init__(self):
        super().__init__(parent=get_maya_main_win())
        self.bookShelf = Bookshelf()
        self.setWindowTitle("Bookshelf Generator")
        self.resize(300, 200)
        self._mk_main_layout()
        self._connect_signals()

    def _connect_signals(self):
        self.cancel_btn.clicked.connect(self.close)
        self.build_btn.clicked.connect(self.build_bookshelf)

    def build_bookshelf(self):
        self.bookShelf.overall_height = self.shelf_height_dspnx.value()
        self.bookShelf.shelf_levels = self.shelf_levels_spnx.value()
        self.bookShelf.generate_bookshelf()

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self._mk_frame_options_ui()
        self._mk_book_options_ui()
        self._mk_buttons_layout()
        self.setLayout(self.main_layout)

    def _mk_frame_options_ui(self):
        self.frame_options_layout = QtWidgets.QHBoxLayout()
        self.shelf_height_lbl = QtWidgets.QLabel("Shelf Height")
        self.shelf_height_dspnx = QtWidgets.QDoubleSpinBox()
        self.shelf_height_dspnx.setMinimumWidth(50)
        self.shelf_height_dspnx.setValue(1.0)
        self.shelf_height_dspnx.setSingleStep(0.1)
        self.frame_options_layout.addWidget(self.shelf_height_lbl)
        self.frame_options_layout.addWidget(self.shelf_height_dspnx)
        self.main_layout.addLayout(self.frame_options_layout)

    def _mk_book_options_ui(self):
        self.book_options_layout = QtWidgets.QHBoxLayout()
        self.book_levels_lbl = QtWidgets.QLabel("Shelf Levels")
        self.shelf_levels_spnx = QtWidgets.QSpinBox()
        self.shelf_levels_spnx.setMinimumWidth(50)
        self.shelf_levels_spnx.setValue(3)
        self.book_options_layout.addWidget(self.book_levels_lbl)
        self.book_options_layout.addWidget(self.shelf_levels_spnx)
        self.main_layout.addLayout(self.book_options_layout)

    def _mk_buttons_layout(self):
        self.build_btn = QtWidgets.QPushButton("Build")
        self.main_layout.addWidget(self.build_btn)

        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.main_layout.addWidget(self.cancel_btn)


class Bookshelf():

    overall_height = 2  # the height of the shelf without the legs

    #shelf_height = overall_height - (overall_height / 62.5)
    shelf_width = 1  # an option
    shelf_depth = 0.3  # an option
    shelf_levels = 6  # an option
    
    #shelf_dividers_height = overall_height / 125
    #shelf_dividers_width = shelf_width - ((overall_height / 125) * 2)
    
    books_offset = 0  # a slider will be added to adjust
    #books_height = ((overall_height - (overall_height / 62.5)) / shelf_levels) - (overall_height / 125)  # a slider will be added to adjust
    #books_depth = shelf_depth - (shelf_depth / 10)  # a slider will be added to adjust

    #shelf_leg_height = overall_height * (1/25)

    def generate_dividers(self):
        dividers = []
        for level in range(1, self.shelf_levels):
            divider = cmds.polyCube(height=(self.overall_height / 125),
                                    width=(self.shelf_width - ((self.overall_height / 125) * 2)),
                                    depth=self.shelf_depth,
                                    name="divider_plank_1")[0]
            cmds.xform(divider,
                       translation=[0,
                                    (((self.overall_height - (self.overall_height / 62.5))/2) +
                                     ((self.overall_height / 125)/2)) -
                                    ((((self.overall_height - (self.overall_height / 62.5)) +
                                       (self.overall_height / 125)) /
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
                leg = cmds.polyCylinder(height=(self.overall_height * (1/25)),
                                        radius=(self.overall_height * (1/25))/2.5,
                                        name="shelf_leg_1")[0]
                cmds.xform(leg,
                           translation=[(((self.shelf_width/2) -
                                        ((self.overall_height / 125) * 4)) *
                                        x_axis_duplicates),
                                        (-self.overall_height/2) -
                                        (self.overall_height * (1/25))/2,
                                        (((self.shelf_depth/2) -
                                         ((self.overall_height / 125) * 4)) *
                                        z_axis_dupllicates),])
                self._freeze_transforms(leg)
                legs.append(leg)

        grp_name = cmds.group(legs, name="Shelf_Legs")
        return grp_name

    def generate_frame(self):
        frame = []
        for duplicates in range(-1, 2, 2):
            vertical_plank = cmds.polyCube(height=(self.overall_height - (self.overall_height / 62.5)),
                                           width=(self.overall_height / 125),
                                           depth=self.shelf_depth,
                                           name="vertical_plank_1")[0]
            cmds.xform(vertical_plank,
                       translation=[((self.shelf_width/2) -
                                    (self.overall_height / 125)/2) *
                                    duplicates,
                                    0, 0])
            self._freeze_transforms(vertical_plank)
            frame.append(vertical_plank)
            horizontal_plank = cmds.polyCube(height=(self.overall_height / 125),
                                             width=self.shelf_width,
                                             depth=self.shelf_depth,
                                             name="horizontal_plank_1")[0]
            cmds.xform(horizontal_plank,
                       translation=[0,
                                    (((self.overall_height - (self.overall_height / 62.5))/2) +
                                     (self.overall_height / 125)/2) *
                                    duplicates,
                                    0])
            self._freeze_transforms(horizontal_plank)
            frame.append(horizontal_plank)

        back_plank = cmds.polyCube(height=self.overall_height,
                                   width=self.shelf_width,
                                   depth=(self.overall_height / 125),
                                   name="back_plank")[0]
        cmds.xform(back_plank,
                   translation=[0,
                                0,
                                -(self.shelf_depth/2) -
                                ((self.overall_height / 125)/2)])
        self._freeze_transforms(back_plank)
        frame.append(back_plank)

        frame.append(self.generate_dividers())
        frame.append(self.generate_legs())
        grp_name = cmds.group(frame, name="Bookshelf_Frame")
        return grp_name

    def generate_books(self):
        pile_of_books = []

        book_x_axis = -((self.shelf_width - ((self.overall_height / 125) * 2))/2) + self.books_offset

        while book_x_axis < ((self.shelf_width - ((self.overall_height / 125) * 2))/2):
            random_width = random.uniform(self.overall_height/100,
                                          self.overall_height/40)
            random_height = random.uniform((((self.overall_height - (self.overall_height / 62.5)) / self.shelf_levels) - (self.overall_height / 125))/1.83529,
                                           (((self.overall_height - (self.overall_height / 62.5)) / self.shelf_levels) - (self.overall_height / 125)))
            random_depth = random.uniform((self.shelf_depth - (self.shelf_depth / 10))/2.16,
                                          (self.shelf_depth - (self.shelf_depth / 10)))

            if book_x_axis + random_width > ((self.shelf_width - ((self.overall_height / 125) * 2))/2):
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
                                    (-(self.shelf_depth - (self.shelf_depth / 10))/2) +
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
                                    (((self.overall_height - (self.overall_height / 62.5))/2) +
                                     ((self.overall_height / 125)/2)) -
                                    ((((self.overall_height - (self.overall_height / 62.5)) +
                                       (self.overall_height / 125)) /
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

        cmds.xform(grp_name,
                   translation=[0,
                                (self.overall_height/2) +
                                (self.overall_height * (1/25)),
                                0])
        cmds.xform(grp_name,
                   pivots=[0,
                           (-self.overall_height/2) -
                           (self.overall_height * (1/25)),
                           0])

        return grp_name

    def _freeze_transforms(self, name):
        cmds.makeIdentity(name, apply=True, translate=True, rotate=True,
                          scale=True, normal=False, preserveNormals=True)
