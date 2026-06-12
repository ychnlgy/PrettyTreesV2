#version 330 core

in vec2 uv;

out vec4 final_color;

uniform sampler2D sprite_texture;

// custom uniforms

uniform float time;

void main() {
    float wave_strength = 0.05;
    float wave_frequency = 10.0;
    float wave_offset = 0.5;

    vec2 sampleUv = vec2(uv.x, 1 - uv.y);
    sampleUv.x += sin(sampleUv.y * wave_frequency + time) * wave_strength * sampleUv.y;
    sampleUv.y += cos(sampleUv.x * wave_frequency + time) * wave_strength * sampleUv.y * wave_offset;
    vec4 col = texture(sprite_texture, sampleUv);
    final_color = vec4(col.rgb, 0.8);
}