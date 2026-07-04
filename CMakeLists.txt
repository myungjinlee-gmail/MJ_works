cmake_minimum_required(VERSION 3.16)

project(MJSDK
    VERSION 0.1.0
    LANGUAGES CXX
)

include(cmake/SdkConfiguration.cmake)

set(SDK_CONFIG "configuration/default.yaml" CACHE FILEPATH "SDK configuration yaml file")

sdk_resolve_configuration_path("${SDK_CONFIG}" SDK_CONFIG_PATH)
sdk_load_configuration("${SDK_CONFIG_PATH}")
sdk_normalize_configuration()

option(SDK_ENABLE_TESTS "Build SDK tests" OFF)

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
message(STATUS "SDK_CONFIG=${SDK_CONFIG_PATH}")
