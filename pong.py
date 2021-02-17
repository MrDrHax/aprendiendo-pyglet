"""
Codigo para correr un pong muy basico, le faltan algunos detalles.

Retos:

Agregar puntuacion
Linea que separe el centro
Hacer que la nueva posicion se calcule dependiendo del tiempo que ha pasado
Hacer que la pantalla quede en distintos colores
Hacer que la pelota cambie de color dependiendo de si esta entre un jugador o no
Hacer que hayan 2 pelotas distintas en el juego al mismo tiempo
Hacer que la pelota se dispare en una direccion aleatoria al iniciar

"""

import pyglet
from pyglet import shapes

class rectangle: # hacemos una clase para guardar variables
    width = 10 # el tamaño del rectangulo en pixeles
    height = 50

class color:
    white = (255,255,255)
    black = (0,0,0)

window = pyglet.window.Window(800, 800, resizable=False, vsync=True)


# creamos a los jugadores, uno de cada lado a la mitad de la pantalla:
player1 = shapes.Rectangle(10, window.height / 2, rectangle.width, rectangle.height, color.white)
player2 = shapes.Rectangle(window.width - 10 - rectangle.width, window.height / 2, rectangle.width, rectangle.height, color.white)

class ball:
    def __init__(self):
        # esto se llama al iniciar la pelota, entonces podemos crear distintas bolas de forma facil

        # primero vamos a crear nuestra pelota

        # creamos posiciones de la pelota que esten a la mitad de la pantalla
        self.x = window.width / 2 
        self.y = window.width / 2

        # y creamos la pelota en su X y Y
        self.ball = shapes.Circle(self.x, self.y, 5, color = color.white)

        # ahora le damos a la pelota una velocidad para que se mueva en ciertos puntos

        self.x_speed = 3
        self.y_speed = 1

    def calcularSiguientePunto(self, context):
        # ahora, ya tenemos nuestra pelota, pero necesitamos que la pelota se mueva y cambie su posicion

        if not (5 < self.x < window.width - 5):
            # si la pelota se esta saliendo de la pantalla, hacemos que valla al otro lado
            self.x_speed *= -1

        if not (5 < self.y < window.height - 5):
            # lo mismo pero para arriba y abajo
            self.y_speed *= -1

        # aqui vemos si va a chocar con algun jugador

        # jugador 1:
        if player1.y < self.y < player1.y + rectangle.height:
            if self.x < 20 and self.x_speed < 0:
                self.x_speed *= -1

        # jugador 2:
        if player2.y < self.y < player2.y + rectangle.height:
            if self.x > window.width - 20 and self.x_speed > 0:
                self.x_speed *= -1

        # cambiamos la pos de x a la nueva
        self.x = self.x + self.x_speed
        self.y = self.y + self.y_speed

        # y hacemos que la posicion se actualize en nuestro objeto

        self.ball.x = self.x
        self.ball.y = self.y

    def draw(self):
        self.ball.draw()

pelota1 = ball() # esto va a crear un objeto de pelota, y va a llamar el __init__ de forma automatica, luego podemos hacer otras cosas abajo

@window.event
def on_draw(): # usamos un decorador para tener un loop que se llama cada vez que dibujamos la pantalla
    '''
    the main pyglet draw function
    '''
    window.clear() # ponemos la pantalla en negro

    # dibujamos los jugadores
    player1.draw() 
    player2.draw()

    # dibujamos la pelota
    pelota1.draw() # nota que esto llama la funcion draw de la clase ball, no directamente el de la pelota

@window.event
def on_mouse_motion(x, y, dx, dy):
    # aqui tomamos la posicion del mouse y la cambiamos a a la del jugador
    player1.y = y

@window.event
def on_key_press(symbol, modifiers):
    # aqui vemos si preciona el teclado hacia arriba o abajo y cambiamos la posicion
    if symbol == pyglet.window.key.UP:
        player2.y += 10
    if symbol == pyglet.window.key.DOWN:
        player2.y -= 10

# llamamos la simulacion de como se mueve la pelota cada 0.02 segundos
pyglet.clock.schedule_interval(pelota1.calcularSiguientePunto, 0.02) 

pyglet.app.run() # al final corremos nuestra app