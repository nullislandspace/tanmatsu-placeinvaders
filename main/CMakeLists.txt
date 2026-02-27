idf_component_register(
	SRCS
		"main.c"
		"game.c"
		"render.c"
		"audio.c"
	PRIV_REQUIRES
		esp_lcd
		nvs_flash
		badge-bsp
	INCLUDE_DIRS
		"."
)

idf_build_set_property(COMPILE_OPTIONS "-Wno-error=unused-variable" APPEND)
idf_build_set_property(COMPILE_OPTIONS "-Wno-error=unused-const-variable" APPEND)
