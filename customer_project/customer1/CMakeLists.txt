add_executable(mj_customer1_app
    src/main.cpp
)
enable_compiler_warnings(mj_customer1_app)

target_include_directories(mj_customer1_app PRIVATE
    "${CMAKE_CURRENT_SOURCE_DIR}/include"
)

target_link_libraries(mj_customer1_app PRIVATE mj_sdk)
