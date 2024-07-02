shader_type spatial;

uniform sampler2D albedo_texture;
uniform sampler2D normal_texture;
uniform sampler2D roughness_texture;
uniform sampler2D ao_texture;
uniform sampler2D displacement_texture;
uniform float displacement_amount : hint_range(0.0, 1.0); // Controla la cantidad de desplazamiento
uniform vec2 uv_scale = vec2(80,80);

void vertex() {
    // Desplazamiento de vértices basado en la textura de desplazamiento
    vec4 displacement = texture(displacement_texture, VERTEX.xy);
    VERTEX += NORMAL * displacement_amount * displacement.r;
}

void fragment() {
	vec2 road_uv = vec2(UV.x * uv_scale.x, UV.y * uv_scale.y);
    vec4 albedo = texture(albedo_texture, road_uv);
    vec3 normal = texture(normal_texture,road_uv).rgb * 2.0 - 1.0; // Mapeo normal requiere conversión de [0,1] a [-1,1]
    float roughness = texture(roughness_texture, road_uv).r;
    float ao = texture(ao_texture, road_uv).r;

    // Mezclar AO con el Albedo
    vec3 final_albedo = albedo.rgb * ao;

    ALBEDO = final_albedo;
    NORMAL = normal;
    ROUGHNESS = roughness;
}