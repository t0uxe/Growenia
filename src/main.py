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
from gi.repository import Gtk, Gio

#from db.db_huerto import DBHuerto

import datetime
import src.db.tablas
from src.db.tablas import Huerto, Planta
import sys


_GLADE_FILE = "src/ui/main.ui"
_DB_PATH = "src/db/main.db"

class MainWindow:
    
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(_GLADE_FILE)
        
        # Recogemos las señales de los widgets
        self.handlers = {
            "on_main_window_destroy": self.on_main_window_destroy,
            "on_btn_ver_huertos_clicked": self.ver_huertos,
            "on_btn_anyadir_huerto_clicked": self.stack_anyadir_huerto,
            "on_btn_guardar_huerto_clicked": self.nuevo_huerto,
            "on_btn_borrar_huerto_clicked": self.borrar_huerto,
            "on_btn_modificar_huerto_clicked": self.stack_modificar_huerto,
            "on_btn_guardar_huerto_modificar_clicked": self.modificar_huerto,
            "on_btn_ver_plantas_clicked": self.ver_plantas,
            "on_btn_guardar_planta_clicked": self.anyadir_planta,
            "on_btn_borrar_planta_clicked": self.borrar_planta,
            "on_btn_anyadir_planta_clicked": self.stack_anyadir_planta,
            "on_btn_modificar_planta_clicked": self.stack_modificar_planta,
            "on_btn_guardar_planta_modificar_clicked": self.modificar_planta,
            "on_btn_about_dialog_clicked": self.mostrar_acerca_de
        }

        # Conectamos las señales al constructor
        self.builder.connect_signals(self.handlers)

        # Recogemos los widgets
        self.header_bar: Gtk.HeaderBar = self.builder.get_object("main_header_bar")
        self.window: Gtk.Window = self.builder.get_object("main_window")
        self.Stack: Gtk.Stack = self.builder.get_object("stack")
        self.tree_view_huertos: Gtk.TreeView = self.builder.get_object("tree_view_huertos")
        self.tree_view_plantas: Gtk.TreeView = self.builder.get_object("tree_view_plantas")
        self.lista_huertos: Gtk.ListStore = self.builder.get_object("lista_huerto")
        self.lista_plantas: Gtk.ListStore = self.builder.get_object("lista_plantas")
        self.btn_ver_huertos = self.builder.get_object("btn_ver_huertos")
        self.btn_anyadir_huerto = self.builder.get_object("btn_anyadir_huerto")
        self.btn_borrar_huerto = self.builder.get_object("btn_borrar_huerto")
        self.btn_ver_plantas = self.builder.get_object("btn_ver_plantas")
        self.btn_about_dialog = self.builder.get_object("btn_about_dialog")

        # Widgets Stack añadir huerto
        self.txt_nombre_huerto = self.builder.get_object("txt_nombre_huerto")
        self.txt_descripcion_huerto = self.builder.get_object("txt_descripcion_huerto")
        self.cal_registrar_huerto = self.builder.get_object("cal_registrar_huerto")

        # Widgets Stack modificar
        self.txt_id_huerto_modificar = self.builder.get_object("txt_id_huerto_modificar")
        self.txt_nombre_modificar = self.builder.get_object("txt_nombre_huerto_modificar")
        self.txt_descripcion_modificar = self.builder.get_object("txt_descripcion_huerto_modificar")
        self.gtkcal_fecha_modificar = self.builder.get_object("cal_registrar_huerto_modificar")
        self.date_cal_modificar = self.builder.get_object("txt_created_at")
        self.btn_modificar_huerto = self.builder.get_object("btn_modificar_huerto")

        # Widgets Stack Añadir Planta        
        self.txt_nombre_planta = self.builder.get_object("txt_nombre_planta")
        self.txt_anotaciones_planta = self.builder.get_object("txt_anotaciones_planta")
        self.cal_registrar_planta = self.builder.get_object("cal_registrar_planta")

        # Widgets Stack Modificar Planta
        self.txt_id_planta_modificar = self.builder.get_object("txt_id_planta_modificar")
        self.txt_modificar_nombre_planta = self.builder.get_object("txt_modificar_nombre_planta")
        self.txt_modificar_anotaciones_planta = self.builder.get_object("txt_modificar_anotaciones_planta")
        self.gtkcal_fecha_modificar_planta = self.builder.get_object("gtkcal_fecha_modificar_planta")
        self.txt_date_cal_modificar_planta = self.builder.get_object("txt_date_cal_modificar_planta")
        self.txt_huerto_id_modificar_planta = self.builder.get_object("txt_huerto_id_modificar_planta")

        self.huerto_activo = 1

        # Mostramos la ventana
        self.window.show_all()
        self.btn_borrar_huerto.hide()
        self.btn_modificar_huerto.hide()
        self.btn_ver_plantas.hide()
        Gtk.main()

    def mensaje(self, texto, descripcion, icono=None):
        mensa: Gtk.MessageDialog = self.builder.get_object("mensaje")
        mensa.props.text = texto
        mensa.props.secondary_text = descripcion
        mensa.props.icon_name = icono
        mensa.show_all()
        mensa.run()
        mensa.hide()

    def mensaje_confirmacion(self, texto, descripcion, icono="gtk-dialog-question"):
        mensa: Gtk.MessageDialog = self.builder.get_object("mensaje_confirmacion")
        mensa.props.text = texto
        mensa.props.secondary_text = descripcion
        mensa.props.icon_name = icono
        mensa.show_all()
        response = mensa.run()
        delete_element = False
        if response == -8: # Pulsa SI
            delete_element = True
        mensa.hide()

        return delete_element

    def select_today(self, calendario):
        """Este método se usa para marcar el día de hoy en el calendario.
        """
        today = datetime.date.today()
        calendario.set_property("day", today.day)
        calendario.set_property("month", today.month-1)
        calendario.set_property("year", today.year)

    def on_main_window_destroy(self, Window):
        """Al cerrar la ventana principal, se finaliza el programa.

        Args:
            Window (obj): Tipo de objeto que contiene la señal
        """
        Gtk.main_quit()

    def stack_anyadir_huerto(self, button):
        self.Stack.set_visible_child_name("stck_anyadir_huerto")

        self.select_today(self.cal_registrar_huerto)

        self.btn_ver_huertos.show()
        self.btn_borrar_huerto.hide()
        self.btn_modificar_huerto.hide()
        self.btn_ver_plantas.hide()     

    def nuevo_huerto(self, button):
        nombre = self.builder.get_object("txt_nombre_huerto")
        descripcion = self.builder.get_object("txt_descripcion_huerto")
        fecha = self.builder.get_object("cal_registrar_huerto").get_date()
        # Sumamos uno al mes porque en Gtk los meses van del 0 al 11...
        fecha = datetime.date(fecha.year, fecha.month+1, fecha.day)

        if not nombre.get_text() or not descripcion.get_text():
            self.mostrar_mensaje_faltan_datos()
        else:
            huerto = Huerto(nombre=nombre.get_text(), descripcion=descripcion.get_text(), fecha_plantacion=fecha)
            huerto.add_huerto()
            self.mensaje("Huerto añadido", "Huerto añadido correctamente.", "gtk-ok")
            nombre.set_text('')
            descripcion.set_text('')

    def ver_huertos(self, button):
        huerto = Huerto()
        huertos = huerto.get_huertos()
        if not huertos:
            usuario_quiere_anyadir_huerto = self.mensaje_confirmacion("No hay huertos en la base de datos", "¿Desea añadir un nuevo huerto?")
            if usuario_quiere_anyadir_huerto:
                self.stack_anyadir_huerto(button)
        
        else:
            self.Stack.set_visible_child_name("stck_ver_huertos")
            self.lista_huertos.clear()
            self.btn_ver_huertos.hide()
            # Mostramos los botones ocultos
            self.btn_borrar_huerto.show()
            self.btn_modificar_huerto.show()
            self.btn_ver_plantas.show()

            for huerto in huertos:            
                fila = []
                fila.append(huerto.id)
                fila.append(huerto.nombre)
                fila.append(huerto.descripcion)
                fila.append(str(huerto.fecha_plantacion))
                fila.append(str(huerto.created_at))
                self.lista_huertos.append(fila)

    def borrar_huerto(self, button):
        model, row = self.tree_view_huertos.get_selection().get_selected()
        if row:
            if self.mensaje_confirmacion("¡Cuidado!", "Se va a borrar el elemento seleccionado. ¿Aceptar?"):
                id_element = model[row][0]
                huerto = Huerto()
                huerto.delete_huerto(id=id_element)
                if not huerto.get_huertos():
                    self.lista_huertos.clear()
                self.ver_huertos(self.btn_ver_huertos)

        else:
            self.mensaje("Error", "Tiene que seleccionar una fila para borrar.", "gtk-dialog-error")
     

    def stack_modificar_huerto(self, button):

        model, row = self.tree_view_huertos.get_selection().get_selected()

        if row:
            id = model[row][0]
            nombre = model[row][1]
            descripcion = model[row][2]
            fecha_plantacion = model[row][3].split('-')
            created_at = model[row][4]

            self.Stack.set_visible_child_name("stck_modificar_huerto")
            self.txt_id_huerto_modificar.set_text(str(id))
            self.txt_nombre_modificar.set_text(nombre)
            self.txt_descripcion_modificar.set_text(descripcion)
            # Se pone la fecha del calendario
            self.gtkcal_fecha_modificar.day = fecha_plantacion[2]
            self.gtkcal_fecha_modificar.month = int(fecha_plantacion[1])-1
            self.gtkcal_fecha_modificar.year = fecha_plantacion[0]
            self.date_cal_modificar.set_text(created_at)

            self.btn_ver_huertos.show()
            self.btn_ver_plantas.hide()
            self.btn_borrar_huerto.hide()
            self.btn_modificar_huerto.hide()

        else:
            self.mensaje("Error", "Tiene que seleccionar una fila para modificar.", "gtk-dialog-error")


    def modificar_huerto(self, button):

        id = int(self.txt_id_huerto_modificar.get_text())
        nombre = self.txt_nombre_modificar.get_text()
        descripcion = self.txt_descripcion_modificar.get_text()
        fecha_plantacion = self.gtkcal_fecha_modificar.get_date()
        fecha_plantacion = datetime.date(fecha_plantacion.year, fecha_plantacion.month+1, fecha_plantacion.day)

        if not nombre or not descripcion:
            self.mostrar_mensaje_faltan_datos()
        else:
            created_at = self.date_cal_modificar.get_text().split('-')
            dia = int(created_at[2])
            mes = int(created_at[1])
            anyo = int(created_at[0])
            created_at = datetime.date(anyo, mes, dia)

            huerto = Huerto(id=id, nombre=nombre, descripcion=descripcion, fecha_plantacion=fecha_plantacion, created_at=created_at)
            huerto.update_huerto()
            self.mensaje("Huerto modificado", "Huerto modificado correctamente.", "gtk-ok")

    def stack_anyadir_planta(self, button):
        self.Stack.set_visible_child_name("stck_anyadir_planta")
        self.select_today(self.cal_registrar_planta)
        self.txt_nombre_planta.set_text('')
        self.txt_anotaciones_planta.set_text('')
        self.btn_ver_plantas.show()
        self.btn_ver_huertos.show()        

    def anyadir_planta(self, button):

        if not self.txt_nombre_planta.get_text() or not self.txt_anotaciones_planta.get_text():
            self.mensaje("Faltan campos", "Por favor, rellene todos los campos.", "gtk-dialog-error")
        else:
            date_cal = self.cal_registrar_planta.get_date()
            fecha = datetime.date(date_cal.year, date_cal.month+1, date_cal.day)

            planta = Planta(nombre=self.txt_nombre_planta.get_text(),
                            anotaciones=self.txt_anotaciones_planta.get_text(),
                            fecha_plantacion=fecha, huerto_id=self.huerto_activo)
            planta.add_planta()
            self.mensaje("Planta añadida", "Planta añadida correctamente.", "gtk-ok")
            self.txt_nombre_planta.set_text('')
            self.txt_anotaciones_planta.set_text('')            
        
    def ver_plantas(self, button):
        model, row = self.tree_view_huertos.get_selection().get_selected()
        try:
            self.huerto_activo = model[row][0] # ID del huerto seleccionado

            planta = Planta()
            plantas = planta.get_plantas(self.huerto_activo)
            if not plantas:
                if self.mensaje_confirmacion("No hay plantas", "Este huerto todavía no tiene plantas. ¿Desea añadir nuevas plantas?"):
                    self.stack_anyadir_planta(button)
            else:
                self.Stack.set_visible_child_name("stck_ver_plantas")
                self.btn_ver_plantas.hide()
                self.btn_ver_huertos.show()                
                self.lista_plantas.clear()
                self.btn_borrar_huerto.hide()
                self.btn_modificar_huerto.hide()

                for planta in plantas:
                    fila = []
                    fila.append(planta.id)
                    fila.append(planta.nombre)
                    fila.append(planta.anotaciones)
                    fila.append(str(planta.fecha_plantacion))
                    fila.append(str(planta.created_at))
                    fila.append(planta.huerto_id)
                    self.lista_plantas.append(fila)

        except TypeError:
            self.mensaje("Error", "Tiene que elegir primero un huerto.", "gtk-dialog-error")

    def borrar_planta(self, button):
        model, row = self.tree_view_plantas.get_selection().get_selected()
        if row:
            if self.mensaje_confirmacion("¡Cuidado!", "Se va a borrar el elemento seleccionado. ¿Aceptar?"):
                id_planta = model[row][0]
                planta = Planta()
                planta.delete_planta(id_planta)
                if not planta.get_plantas(self.huerto_activo):
                    self.lista_plantas.clear()
                self.ver_plantas(self.btn_ver_plantas)

        else:
            self.mensaje("Error", "Tiene que seleccionar una fila para borrar.", "gtk-dialog-error")


    def stack_modificar_planta(self, button):

        model, row = self.tree_view_plantas.get_selection().get_selected()

        if row:
            id = model[row][0]
            nombre = model[row][1]
            anotaciones = model[row][2]
            fecha_plantacion = model[row][3].split('-')
            created_at = model[row][4]
            huerto_id = str(model[row][5])

            self.Stack.set_visible_child_name("stck_modificar_planta")
            self.txt_id_planta_modificar.set_text(str(id))
            self.txt_modificar_nombre_planta.set_text(nombre)
            self.txt_modificar_anotaciones_planta.set_text(anotaciones)
            # Se pone la fecha del calendario
            self.gtkcal_fecha_modificar_planta.day = fecha_plantacion[2]
            self.gtkcal_fecha_modificar_planta.month = int(fecha_plantacion[1])-1
            self.gtkcal_fecha_modificar_planta.year = fecha_plantacion[0]
            self.txt_date_cal_modificar_planta.set_text(created_at)
            self.txt_huerto_id_modificar_planta.set_text(huerto_id)

            self.btn_ver_huertos.show()
            self.btn_ver_plantas.hide()
            self.btn_borrar_huerto.hide()
            self.btn_modificar_huerto.hide()

        else:
            self.mensaje("Error", "Tiene que seleccionar una fila para modificar.", "gtk-dialog-error")

    def mostrar_mensaje_faltan_datos(self):
        self.mensaje("Faltan datos", "Por favor, rellene los campos.", "gtk-dialog-error")

    def modificar_planta(self, button):
        id = int(self.txt_id_planta_modificar.get_text())
        nombre = self.txt_modificar_nombre_planta.get_text()
        anotaciones = self.txt_modificar_anotaciones_planta.get_text()
        fecha_plantacion = self.gtkcal_fecha_modificar_planta.get_date()
        fecha_plantacion = datetime.date(fecha_plantacion.year, fecha_plantacion.month+1, fecha_plantacion.day)
        huerto_id = int(self.txt_huerto_id_modificar_planta.get_text())

        if not nombre or not anotaciones:
            self.mostrar_mensaje_faltan_datos()
        else:
            created_at = self.txt_date_cal_modificar_planta.get_text().split('-')
            dia = int(created_at[2])
            mes = int(created_at[1])
            anyo = int(created_at[0])
            created_at = datetime.date(anyo, mes, dia)

            planta = Planta(id=id, nombre=nombre, anotaciones=anotaciones, fecha_plantacion=fecha_plantacion, created_at=created_at, huerto_id=huerto_id)
            planta.update_planta()
            self.mensaje("Planta modificada", "Planta modificada correctamente.", "gtk-ok")


    def mostrar_acerca_de(self, button):
        ventana = self.builder.get_object("window_about_dialog")
        ventana.show_all()
        ventana.run()
        ventana.hide()
