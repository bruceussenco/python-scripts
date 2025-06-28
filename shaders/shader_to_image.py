import pygame
import moderngl
import sys
from array import array

image_path  = input("image path: ")
output_path = "edited_" + image_path

smoothstep_min = input("smoothstep_min: ")
smoothstep_max = input("smoothstep_max: ")

uv_shader_choice = input("""--- uv shader ---
0. nothing
1. uv -> rg
: """)

# ----- Início do Processamento Headless -----
pygame.init()

# Carregar a imagem com Pygame
try:
    img = pygame.image.load(image_path)
except pygame.error:
    print(f"Erro ao carregar a imagem: {image_path}")
    pygame.quit()
    sys.exit()

screen_width, screen_height = img.get_size()

# ----- contexto ModernGL headless -----
try:
    # Tenta criar um contexto usando EGL (Linux/Windows com drivers específicos)
    ctx = moderngl.create_context(standalone=True)
    print("Contexto ModernGL headless criado com EGL.")
except Exception as e:
    print(f"Erro ao criar contexto headless com EGL: {e}")
    try:
        # Tenta criar um contexto usando OSMesa (Linux/macOS, geralmente)
        # Pode exigir instalação de 'libosmesa-dev' ou similar
        import moderngl_window.context.headless
        window = moderngl_window.context.headless.Window(size=(screen_width, screen_height))
        ctx = window.ctx
        print("Contexto ModernGL headless criado com OSMesa.")
    except Exception as e:
        print(f"Erro ao criar contexto headless com OSMesa: {e}")
        print("Não foi possível criar um contexto OpenGL headless.")
        print("Por favor, verifique se você tem as bibliotecas EGL ou OSMesa instaladas e configuradas.")
        print("Em alguns casos, pode ser necessário abrir uma janela invisível (Opção 2).")
        pygame.quit()
        sys.exit()

# esse framebuffer object (FBO) é a "tela" para renderização
color_attachment = ctx.texture((screen_width, screen_height), 4)
fbo = ctx.framebuffer(color_attachment)

# ----- shaders glsl -----
vertex_shader_code = """
#version 330 core
in vec2 in_vert;
in vec2 in_texcoord;
out vec2 inv_uv;
void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
    inv_uv = in_texcoord;
}
"""
fragment_shader_code = """
#version 330 core
uniform sampler2D tex;
in vec2 inv_uv;
out vec4 out_color;
void main() {
    vec4 color = texture(tex, inv_uv);
    vec2 uv = inv_uv;
    uv.y = 1.0 - uv.y;

    float gray = 0.2126*color.r + 0.7152*color.g + 0.0722*color.b;
"""
fragment_shader_code += f"color = vec4(vec3(smoothstep({smoothstep_min}, {smoothstep_max}, gray)), 1.0);"
if uv_shader_choice == "1":
    fragment_shader_code += "color.b *= 1.0 - uv.x;\ncolor.g *= 1.0 - uv.y;"
fragment_shader_code += """
    out_color = color;
}
"""
program = ctx.program(vertex_shader=vertex_shader_code, fragment_shader=fragment_shader_code)

quad_vertices = [
    -1.0, -1.0,  0.0, 0.0,  # Bottom-left
     1.0, -1.0,  1.0, 0.0,  # Bottom-right
    -1.0,  1.0,  0.0, 1.0,  # Top-left
     1.0,  1.0,  1.0, 1.0,  # Top-right
]
quad_vbo = ctx.buffer(data=array("f", quad_vertices))
render_object = ctx.vertex_array(
    program,
    [(quad_vbo, '2f 2f', 'in_vert', 'in_texcoord')]
)

# ligar o FBO e renderizar
fbo.use() # comece a renderizar para o FBO
ctx.clear(0.0, 0.0, 0.0, 1.0) # limpe o FBO

# converter a imagem Pygame em textura e usar
texture_data = pygame.image.tostring(img, "RGBA", True)
img_texture = ctx.texture(img.get_size(), 4, texture_data)
img_texture.use(0)
program["tex"] = 0

# renderizar o objeto com o shader no FBO
render_object.render(mode=moderngl.TRIANGLE_STRIP)

# ----- salvar imagem -----
# ler os pixels do FBO
buffer = fbo.read(components=4)

# superfície Pygame com os pixels lidos
screenshot_surface = pygame.image.frombuffer(buffer, (screen_width, screen_height), "RGBA")
screenshot_surface = pygame.transform.flip(screenshot_surface, False, True)

# salvar
pygame.image.save(screenshot_surface, output_path)
print(f"Imagem com shader salva como {output_path}")

# ----- limpeza -----
img_texture.release()
fbo.release()
color_attachment.release()
ctx.release()
pygame.quit()
sys.exit()

