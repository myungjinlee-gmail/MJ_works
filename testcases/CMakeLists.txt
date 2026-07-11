include(GoogleTest)

add_subdirectory(src)
add_subdirectory(sdk)
add_subdirectory(customer_project)

add_executable(google_test_smoke_test
    google_test_smoke_test.cpp
)

target_link_libraries(google_test_smoke_test
    PRIVATE
        GTest::gtest_main
)

gtest_discover_tests(google_test_smoke_test)

find_program(TEST_BASH_EXECUTABLE bash)

if(NOT TEST_BASH_EXECUTABLE)
    message(FATAL_ERROR "bash is required to run bootstrap tests")
endif()

add_test(
    NAME setup_dev_bootstrap
    COMMAND "${TEST_BASH_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/scripts/setup_dev_test.sh"
)

add_test(
    NAME yaml_cmake_configuration
    COMMAND "${TEST_BASH_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/scripts/cmake_configuration_test.sh"
)
