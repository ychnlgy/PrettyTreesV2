#version 330 core

in vec2 uv;

out vec4 final_color;

uniform sampler2D sprite_texture;

void main() {
    vec2 sampleUv = vec2(uv.x, 1 - uv.y);
    vec4 col = texture(sprite_texture, sampleUv);
    final_color = vec4(col.rgb, 0.3);
}