#version 330 core

in vec2 uv;

out vec4 final_color;

uniform sampler2D sprite_texture;

void main() {
    vec4 tex_color = texture(sprite_texture, uv);
    final_color = tex_color;
}