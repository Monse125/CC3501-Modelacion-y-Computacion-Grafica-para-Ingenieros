shader_type spatial;

uniform sampler2D road_texture;
uniform vec2 uv_scale = vec2(0.1,8);

void fragment() {
    // Rotar las coordenadas UV
    vec2 road_uv = vec2(UV.y * uv_scale.y, UV.x * uv_scale.x); // Intercambia x e y para rotar la textura

    vec4 color = texture(road_texture, road_uv);
    ALBEDO = color.rgb;
    METALLIC = 0.0;
    ROUGHNESS = 0.9;
}