import pygame
import moderngl
import sys
from array import array

# --- Configurações da Imagem e Shader ---
image_path  = input("image path: ")
output_path = "edited_" + image_path

# --- Funções Auxiliares ---
def surf_to_texture(surf, ctx):
    texture_data = pygame.image.tostring(surf, "RGBA", True)
    texture = ctx.texture(surf.get_size(), 4, texture_data)
    return texture

# --- Início do Processamento Headless ---
pygame.init()

# Carregar a imagem com Pygame
try:
    img = pygame.image.load(image_path)
except pygame.error:
    print(f"Erro ao carregar a imagem: {image_path}")
    pygame.quit()
    sys.exit()

screen_width, screen_height = img.get_size()

# 1. Crie um contexto ModernGL headless
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

# 2. Crie um Framebuffer Objeto (FBO) para renderizar para ele
# Este FBO atuará como sua "tela" fora da janela
color_attachment = ctx.texture((screen_width, screen_height), 4) # 4 componentes para RGBA
fbo = ctx.framebuffer(color_attachment)



# 4. Configure seu shader e objetos de renderização ModernGL
# (Adapte esta seção ao seu código real do shader)
# Exemplo básico:
vertex_shader_code = """
#version 330 core
in vec2 in_vert;
in vec2 in_texcoord;
out vec2 v_texcoord;
void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
    v_texcoord = in_texcoord;
}
"""
fragment_shader_code = """
#version 330 core
uniform sampler2D tex;
in vec2 v_texcoord;
out vec4 out_color;
void main() {
    out_color = texture(tex, v_texcoord);
    // ADICIONE SEU EFEITO SHADER AQUI
    // Exemplo de shader simples: inverter cor
    //out_color = vec4(1.0 - out_color.rgb, out_color.a);
}
"""
program = ctx.program(vertex_shader=vertex_shader_code, fragment_shader=fragment_shader_code)

quad_vertices = [
    -1.0, -1.0,  0.0, 0.0,  # Bottom-left
     1.0, -1.0,  1.0, 0.0,  # Bottom-right
    -1.0,  1.0,  0.0, 1.0,  # Top-left
     1.0,  1.0,  1.0, 1.0,  # Top-right
]
#quad_vbo = ctx.buffer(data=bytearray(quad_vertices))
quad_vbo = ctx.buffer(data=array("f", quad_vertices))
render_object = ctx.vertex_array(
    program,
    [(quad_vbo, '2f 2f', 'in_vert', 'in_texcoord')]
)

# 5. Ligar o FBO e renderizar
fbo.use() # Comece a renderizar para o FBO, não para a tela
ctx.clear(0.0, 0.0, 0.0, 1.0) # Limpe o FBO

# Converta a imagem Pygame em textura e use-a
img_texture = surf_to_texture(img, ctx)
img_texture.use(0)
program["tex"] = 0

# Renderize o objeto com o shader no FBO
render_object.render(mode=moderngl.TRIANGLE_STRIP)

# 6. Ler os pixels do FBO
# 'read()' do FBO
buffer = fbo.read(components=3) # Ou 4 se seu shader ou textura usa RGBA

# 7. Crie a superfície Pygame a partir dos pixels lidos
screenshot_surface = pygame.image.frombuffer(buffer, (screen_width, screen_height), "RGB") # Use "RGBA" se 'components=4'

# 8. Inverta verticalmente (OpenGL é bottom-up, Pygame é top-down)
screenshot_surface = pygame.transform.flip(screenshot_surface, False, True)

# 9. Salve a imagem
pygame.image.save(screenshot_surface, output_path)
print(f"Imagem com shader salva como {output_path}")

# --- Limpeza ---
img_texture.release()
fbo.release()
color_attachment.release()
ctx.release()
pygame.quit()
sys.exit()

