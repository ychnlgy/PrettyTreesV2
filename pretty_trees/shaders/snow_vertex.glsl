#version 330 core

in vec3 position;
in vec3 translate;
in vec3 tex_coords;

out vec2 uv;

uniform WindowBlock {
    mat4 projection;
    mat4 view;
} window;

void main() {
    gl_Position = window.projection * window.view * vec4(position + translate, 1.0);
    uv = vec2(tex_coords.x, 1.0-tex_coords.y);
}