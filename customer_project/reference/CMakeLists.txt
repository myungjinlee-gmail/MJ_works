add_executable(mj_reference_app
    src/main.cpp
)
enable_compiler_warnings(mj_reference_app)

target_link_libraries(mj_reference_app PRIVATE mj_sdk)

add_subdirectory(src)
add_subdirectory(capture)
add_subdirectory(display)
add_subdirectory(draw)
