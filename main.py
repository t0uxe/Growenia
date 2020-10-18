

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

gladefile = "ui/main.glade"
builder = Gtk.Builder()
builder.add_from_file(gladefile)
window = builder.get_object("main_window")
window.
if (window):
  window.connect("destroy", Gtk.main_quit)

window.show_all()
Gtk.main()
