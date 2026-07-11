cmake_minimum_required(VERSION 3.16)

project(MJSDK
    VERSION 0.1.0
    LANGUAGES CXX
)

include(cmake/SdkConfiguration.cmake)

set(SDK_CONFIG "configuration/default.yaml" CACHE FILEPATH "SDK configuration yaml file")

sdk_resolve_configuration_path("${SDK_CONFIG}" SDK_CONFIG_PATH)
sdk_load_configuration("${SDK_CONFIG_PATH}")
sdk_define_boolean_option(
    SDK_RUN_DEV_SETUP
    "Run development environment setup during configure"
    OFF
)
sdk_define_boolean_option(
    SDK_ENABLE_TESTS
    "Build SDK tests"
    OFF
)
sdk_normalize_configuration()

if(SDK_RUN_DEV_SETUP)
    if(DEFINED ENV{CI} OR DEFINED ENV{GITHUB_ACTIONS})
        message(STATUS "Skipping development setup in CI")
    else()
        find_program(BASH_EXECUTABLE bash)

        if(NOT BASH_EXECUTABLE)
            message(FATAL_ERROR "bash is required to run scripts/setup_dev.sh")
        endif()

        execute_process(
            COMMAND "${BASH_EXECUTABLE}" "${CMAKE_SOURCE_DIR}/scripts/setup_dev.sh"
            WORKING_DIRECTORY "${CMAKE_SOURCE_DIR}"
            RESULT_VARIABLE SDK_DEV_SETUP_RESULT
        )

        if(NOT SDK_DEV_SETUP_RESULT EQUAL 0)
            message(FATAL_ERROR "scripts/setup_dev.sh failed")
        endif()
    endif()
endif()

add_subdirectory(src)
add_subdirectory(customer_project)

if(SDK_ENABLE_TESTS)
    enable_testing()
    add_subdirectory(testcases)
endif()

message(STATUS "SDK_HW_TARGET=${SDK_HW_TARGET} canonical=${SDK_HW_TARGET_CANONICAL}")
message(STATUS "SDK_OS_TARGET=${SDK_OS_TARGET} canonical=${SDK_OS_TARGET_CANONICAL}")
message(STATUS "SDK_PROJECT_TARGET=${SDK_PROJECT_TARGET}")
message(STATUS "SDK_CAPTURE_TARGET=${SDK_CAPTURE_TARGET} canonical=${SDK_CAPTURE_TARGET_CANONICAL}")
message(STATUS "SDK_DISPLAY_TARGET=${SDK_DISPLAY_TARGET} canonical=${SDK_DISPLAY_TARGET_CANONICAL}")
message(STATUS "SDK_RUN_DEV_SETUP=${SDK_RUN_DEV_SETUP}")
message(STATUS "SDK_ENABLE_TESTS=${SDK_ENABLE_TESTS}")
message(STATUS "SDK_CONFIG=${SDK_CONFIG_PATH}")
