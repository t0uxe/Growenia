# This file is part of Growenia.

# Growenia is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Growenia is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Growenia.  If not, see <https://www.gnu.org/licenses/>.

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk



#UI_PATH = "/home/aragorn/Documentos/Proyecto_FOC/Fase2/growenia/src/ui/"
#UI_FILE_MAIN_WINDOW = "/home/aragorn/Documentos/Proyecto_FOC/Fase2/growenia/src/ui/main.ui"
_GLADE_FILE = "src/ui/main.ui"

class MainWindow:
    
    def __init__(self):
        self.builder = Gtk.Builder()
        #self.builder.add_from_file(UI_FILE_MAIN_WINDOW)
        self.builder.add_from_file(_GLADE_FILE)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("main_window")
        self.window.show_all()
        Gtk.main()

    def destroy(self):
        self.window.connect("destroy", Gtk.main_quit)
        
    def start(self):
        pass
