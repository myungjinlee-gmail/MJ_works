add_library(mj_sdk SHARED)
enable_compiler_warnings(mj_sdk)

target_include_directories(mj_sdk
    PUBLIC
        "${PROJECT_SOURCE_DIR}/include"
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}"
)

target_compile_features(mj_sdk PUBLIC cxx_std_11)

set_target_properties(mj_sdk PROPERTIES
    CXX_STANDARD 11
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
    OUTPUT_NAME "mj_sdk"
)

add_subdirectory(foundations)
add_subdirectory(algorithm)
add_subdirectory(osal)
add_subdirectory(hwal)
add_subdirectory(algorithm_hwal)
add_subdirectory(sdk)
