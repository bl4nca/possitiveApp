# main.py
import json
from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock



# Cargar frases desde un archivo JSON
def cargar_frases(idioma):
    with open('frases.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data[idioma]['frases']


# Obtener la frase del día
def obtener_frase_del_dia(frases):
    dia_del_año = datetime.now().timetuple().tm_yday
    return frases[dia_del_año - 1]


class PantallaSeleccionIdioma(Screen):
    def __init__(self, app, **kwargs):
        super(PantallaSeleccionIdioma, self).__init__(**kwargs)
        self.app = app

    def seleccionar_idioma(self, idioma):
        # Cambia el idioma y actualiza la frase
        self.app.idioma_actual = idioma
        self.app.frases = cargar_frases(idioma)
        self.app.frase_del_dia = obtener_frase_del_dia(self.app.frases)
        self.app.mostrar_pantalla_frase()


class PantallaFraseDia(Screen):
    def __init__(self, app, **kwargs):
        super(PantallaFraseDia, self).__init__(**kwargs)
        self.app = app

    def on_pre_enter(self):
        # Actualiza la frase del día antes de mostrar la pantalla
        self.ids.label_frase.text = self.app.frase_del_dia


class MyApp(App):
    def build(self):

        self.idioma_actual = 'es'
        self.frases = []
        self.frase_del_dia = ''

        # Crear el ScreenManager y agregar las pantallas
        self.sm = ScreenManager()
        self.pantalla_idioma = PantallaSeleccionIdioma(self, name='seleccion_idioma')
        self.pantalla_frase_dia = PantallaFraseDia(self, name='frase_dia')

        self.sm.add_widget(self.pantalla_idioma)
        self.sm.add_widget(self.pantalla_frase_dia)

        return self.sm

    def mostrar_pantalla_frase(self):
        # Cambia a la pantalla de la frase del día
        self.sm.current = 'frase_dia'


if __name__ == '__main__':
    MyApp().run()