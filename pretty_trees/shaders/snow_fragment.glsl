#version 330 core

in vec2 uv;

uniform float time;

float rand(vec2 co) {
    return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
    vec3 snow_color = vec3(1.0);
    vec4 final_color = vec4(0.0);

    // Number of snow layers to create a sense of depth
    const int layers = 5;
    const float inv_layers = 1.0 / float(layers);
    
    for (int i = 0; i < layers; ++i) {
        float depth = float(i) * inv_layers;
        float scale = 10.0 / (depth * 4.0 + 1.0);
        float speed = (depth * 0.5 + 0.5);
        
        vec2 pos = uv * scale;
        pos.y -= time * speed; // Falling motion
        pos.x += sin(time + depth * 10.0) * 0.2; // Swaying motion
        
        // Generate snowflake coordinates
        vec2 ipos = floor(pos);
        vec2 fpos = fract(pos);
        
        vec2 center = vec2(rand(ipos + vec2(100.0, 0.0)), rand(ipos + vec2(0.0, 100.0)));
        float dist = distance(fpos, center);
        float radius = (depth * 0.02) + 0.02;
        
        if (dist < radius) {
            float intensity = (1.0 - (dist / radius)) * (1.0 - pow(uv.y, depth + inv_layers));
            final_color += vec4(snow_color, intensity * (1.0 - depth));
        }
    }
    
    gl_FragColor = vec4(1.0 - final_color.rgb, final_color.a); // Invert colors for white snow on black background
}
