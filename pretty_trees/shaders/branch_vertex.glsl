#version 330 core

in vec3 position;
in vec2 anchor_position;
in vec3 translate;
in vec3 tex_coords;

in vec2 scale;

in float rotation;  // radians

out vec2 uv;
out float depth;

uniform WindowBlock
{
    mat4 projection;
    mat4 view;
} window;

void main() {
    mat2 rotationMatrix = mat2(cos(rotation), -sin(rotation), sin(rotation), cos(rotation));
    vec2 rotated = rotationMatrix * ((position.xy - anchor_position) * scale);
    vec2 final = rotated + translate.xy;

    gl_Position = window.projection * window.view * vec4(final, position.z + translate.z, 1.0);
    uv = tex_coords.xy;
    depth = translate.z;
}
