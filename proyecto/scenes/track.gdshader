shader_type spatial;

uniform sampler2D road_texture;
uniform vec2 uv_scale = vec2(0.19, 8);

void fragment() {
    vec2 road_uv = vec2(UV.y * uv_scale.y, UV.x * uv_scale.x);
    vec4 color = texture(road_texture, road_uv);
    ALBEDO = color.rgb;
    METALLIC = 0.0;
    ROUGHNESS = 0.8;
}