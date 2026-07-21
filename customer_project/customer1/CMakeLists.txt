add_executable(mj_customer1_app
    src/main.cpp
)
enable_compiler_warnings(mj_customer1_app)

target_include_directories(mj_customer1_app PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)

target_link_libraries(mj_customer1_app PRIVATE mj_sdk)
target_compile_features(mj_customer1_app PRIVATE cxx_std_17)

set_target_properties(mj_customer1_app PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
)
