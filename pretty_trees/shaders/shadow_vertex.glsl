#version 330 core

in vec3 position;
in vec3 translate;
in vec3 tex_coords;

out vec2 uv;

uniform WindowBlock
{
    mat4 projection;
    mat4 view;
} window;

// custom uniforms
uniform float progress;
uniform float progress_slope;

void main() {
    mat4 transform = window.projection * window.view;
    vec4 translated = transform * vec4(position + translate, 1.0);

    // shear only the top half (i.e. v < 0.5)
    if (tex_coords.y < 0.5) {
        vec4 untranslated = transform * vec4(position, 1.0);
        float p = (progress * 2 - 1) * progress_slope;
        translated.x += p * untranslated.y;
    }
    
    gl_Position = translated;
    uv = tex_coords.xy;
}
