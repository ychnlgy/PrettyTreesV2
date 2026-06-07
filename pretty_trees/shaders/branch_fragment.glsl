#version 330 core

in vec2 uv;
in float depth;

out vec4 final_color;

uniform sampler2D sprite_texture;

// custom uniforms
uniform vec2 branch_curvature_origin;
uniform float branch_curvature_radius;
uniform float depth_effect_multiplier;

void main() {
    // check if uv.y is outside of the circle defined by branch_curvature
    float dy2 = pow(branch_curvature_radius, 2) - pow(uv.x - branch_curvature_origin.x, 2);
    float maxY = branch_curvature_origin.y - sqrt(dy2);

    vec4 tex_color = texture(sprite_texture, uv);
    float depth_effect = depth_effect_multiplier * depth;
    tex_color.r = clamp(tex_color.r + depth_effect, 0.0, 1.0);
    tex_color.g = clamp(tex_color.g + depth_effect, 0.0, 1.0);
    tex_color.b = clamp(tex_color.b + depth_effect, 0.0, 1.0);

    // in the future, we'll curve it
    final_color = abs(uv.y - 0.5) < (maxY - 0.5) ? tex_color : vec4(0, 0, 0, 0);
}