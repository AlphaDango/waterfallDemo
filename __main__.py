import pygame
from pygame.locals import *
from sys import exit
from OpenGL.GL import *
from OpenGL.GL import shaders
from numpy import array

VERTEX_SHADER = """
#version 420 core
layout(location = 0) in vec3 vPos;
void main()
{
    gl_Position = vec4(vPos, 1);
}
"""

FRAGMENT_SHADER = """
#version 420 core
#define fragCoord gl_FragCoord.xy
uniform float iTime;
uniform vec2  iResolution;
out vec4 O;

#define rand(U)  fract(sin(dot(U ,vec2(13.0,78.0)))* 4048) //Zufallszahl durch dot Produkt des gegeben Vectors in einer Sinusfunktion

void main()
{
	vec2 U = 3*(fragCoord.xy / iResolution.xy); // Horizontale aufteilung (in diesen Fall 3 Teilungen)
    float rY = U.y - rand(vec2(U.x, floor(U.y))) / 5 + iTime * 5, //Varianz und Geschwindikgeit
           s = 1.3 - fract(rY); //Helligkeit
    
	O = vec4(1,1,1,1) - s * vec4(1,.7,0,1); //Farbverlauf (Weiß zu Blau)
}
"""

class Main(object):
    def __init__(self):
        pygame.init()
        self.resolution = 800, 600
        pygame.display.set_mode(self.resolution, DOUBLEBUF | OPENGL)

        self.vertex_shader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
        self.fragment_shader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(self.vertex_shader, self.fragment_shader)

        self.uni_ticks = glGetUniformLocation(self.shader, 'iTime')

        glUseProgram(self.shader)
        glUniform2f(glGetUniformLocation(self.shader, 'iResolution'), *self.resolution)

        self.vertices = array([-1, -1, 0,
                               1, -1, 0,
                               1, 1, 0,
                               -1, 1, 0], dtype='int')

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_INT, GL_FALSE, 0, None)

        self.clock = pygame.time.Clock()

    def loop(self):
        while True:
            self.clock.tick(8192)

            glClear(GL_COLOR_BUFFER_BIT)

            for event in pygame.event.get():
                if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    exit()

            glUseProgram(self.shader)

            glUniform1f(self.uni_ticks, pygame.time.get_ticks() / 1000.0)

            glBindVertexArray(self.vao)
            glDrawArrays(GL_QUADS, 0, 4)

            pygame.display.set_caption("FPS: {}".format(self.clock.get_fps()))
            pygame.display.flip()


if __name__ == '__main__':
    Main().loop()
