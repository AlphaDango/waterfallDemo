
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GL import shaders

from sys import exit as exitsystem

from numpy import array

VERTEX_SHADER = """
#version 420 core
layout(location = 0) in vec3 vPos;
void main()
{
    gl_Position = vec4(vPos, 1.0);
}
"""

FRAGMENT_SHADER = """
#version 420 core
#define fragCoord gl_FragCoord.xy
uniform vec2  iMouse;
uniform float iTime;
uniform vec2  iResolution;
out vec4 fragColor;

float rand(vec2 co){
    return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
}

void main()
{
    vec2 uv = fragCoord.xy / iResolution.xy;
    
    uv *= 3.0;
    
   
    float randY = uv.y - rand(vec2(uv.x, floor(uv.y))) * 0.2 + iTime * 5.;
    float g = fract(randY);
    float r = floor(randY);
    
    float c = g - rand(vec2(uv.x, r)) * 0.1;
    float s = 1. - fract(c);
    
	fragColor =  vec4(0.93, 0.97, 1, 1) - s * vec4(0.7, 0.3, 0.1, 0);;
}
"""


class Main(object):
    def __init__(self):
        pygame.init()
        self.resolution = 1280, 720
        pygame.display.set_mode(self.resolution, DOUBLEBUF | OPENGL)
        pygame.display.set_caption('PyShadeToy')

        # Shaders
        self.vertex_shader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
        self.fragment_shader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

        # Shader program which hosts the vertex and fragment shader
        self.shader = shaders.compileProgram(self.vertex_shader, self.fragment_shader)

        # Get the uniform locations
        self.uni_ticks = glGetUniformLocation(self.shader, 'iTime')

        glUseProgram(self.shader)  # Need to be enabled before sending uniform variables
        # Resolution doesn't change. Send it once
        glUniform2f(glGetUniformLocation(self.shader, 'iResolution'), *self.resolution)

        # Create the fullscreen quad for drawing
        self.vertices = array([-1.0, -1.0, 0.0,
                               1.0, -1.0, 0.0,
                               1.0, 1.0, 0.0,
                               -1.0, 1.0, 0.0], dtype='float32')

        # Generate VAO
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        # Generate VBO which is stored in the VAO state
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        self.clock = pygame.time.Clock()

    def mainloop(self):
        while 1:
            delta = self.clock.tick(8192)

            glClearColor(0.0, 0.0, 0.0, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            for event in pygame.event.get():
                if (event.type == QUIT) or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    exitsystem()

            glUseProgram(self.shader)

            # Send uniform values
            glUniform1f(self.uni_ticks, pygame.time.get_ticks() / 1000.0)

            # Bind the vao (which stores the VBO with all the vertices)
            glBindVertexArray(self.vao)
            glDrawArrays(GL_QUADS, 0, 4)

            pygame.display.set_caption("FPS: {}".format(self.clock.get_fps()))
            pygame.display.flip()


if __name__ == '__main__':
    Main().mainloop()
