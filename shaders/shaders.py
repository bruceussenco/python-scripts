import sys
from array import array

import pygame
import moderngl

pygame.init()

img_path = input("image path: ")
output_path = "edited_" + img_path
img = pygame.image.load(img_path)
width, height = img.get_size()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface((width, height))
ctx = moderngl.create_context()

clock = pygame.time.Clock()


quad_buffer = ctx.buffer(data=array("f", [
    # position (x, y), uv coords (x, y)
    -1.0,  1.0, 0.0, 0.0, # topleft
     1.0,  1.0, 1.0, 0.0, # topright
    -1.0, -1.0, 0.0, 1.0, # bottomleft
     1.0, -1.0, 1.0, 1.0, # bottomright
]))

vert_shader = """
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
"""

frag_shader = """
#version 330 core

uniform sampler2D tex;
uniform float time;

in vec2 uvs;
out vec4 f_color;

void main() {
    vec2 sample_pos = vec2(uvs.x, uvs.y);

    vec4 color = texture(tex, sample_pos);

    color.r *= uvs.x;
    color.g *= uvs.y;

    f_color = color;
}
"""

program = ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
render_object = ctx.vertex_array(program, [(quad_buffer, "2f 2f", "vert", "texcoord")])

def surf_to_texture(surf):
    """tex = ctx.texture(surf.get_size(), 4)
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    tex.swizzle = "BGRA"
    tex.write(surf.get_view("1"))"""
    texture_data = pygame.image.tostring(surf, "RGBA", True)
    tex = ctx.texture(surf.get_size(), 4, texture_data)
    return tex

running = True
while running:
    display.fill((0, 0, 0))
    display.blit(img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                # O ModernGL renderiza para o framebuffer padrão, que é o que você vê na tela
                buffer = ctx.fbo.read(viewport=(0, 0, width, height), components=3)

                screenshot_surface = pygame.image.frombuffer(buffer, (width, height), "RGB")
                #todo check this flip
                screenshot_surface = pygame.transform.flip(screenshot_surface, False, True)

                pygame.image.save(screenshot_surface, output_path)
                print("Screenshot salvo como", output_path)

    #todo check this flip
    display = pygame.transform.flip(display, False, True)
    
    ctx.clear(0.0, 0.0, 0.0, 1.0)
    frame_tex = surf_to_texture(display)
    frame_tex.use(0)
    program["tex"] = 0
    render_object.render(mode=moderngl.TRIANGLE_STRIP)

    pygame.display.flip()
    frame_tex.release()
    clock.tick(60)

pygame.quit()
sys.exit()

