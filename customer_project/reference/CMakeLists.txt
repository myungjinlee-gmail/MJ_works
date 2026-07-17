add_executable(mj_reference_app
    src/main.cpp
)
enable_compiler_warnings(mj_reference_app)

target_link_libraries(mj_reference_app PRIVATE mj_sdk)
target_compile_features(mj_reference_app PRIVATE cxx_std_11)

set_target_properties(mj_reference_app PROPERTIES
    CXX_STANDARD 11
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
)

add_subdirectory(src)
add_subdirectory(capture)
add_subdirectory(display)
add_subdirectory(draw)
