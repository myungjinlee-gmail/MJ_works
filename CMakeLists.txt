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

add_library(mj_sdk SHARED
    src/sdk/sdk_api.cpp
    src/sdk/${SDK_HW_TARGET_CANONICAL}/sdk_backend_stub.cpp
    src/osal/${SDK_OS_TARGET_CANONICAL}/osal_stub.cpp
    src/hwal/${SDK_HW_TARGET_CANONICAL}/hwal_stub.cpp
    src/algorithm_hwal/${SDK_HW_TARGET_CANONICAL}/algorithm_hwal_stub.cpp
)

target_include_directories(mj_sdk
    PUBLIC
        "${CMAKE_CURRENT_SOURCE_DIR}/include"
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/src"
)

target_compile_features(mj_sdk PUBLIC cxx_std_11)

set_target_properties(mj_sdk PROPERTIES
    CXX_STANDARD 11
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
    OUTPUT_NAME "mj_sdk"
)

if(SDK_PROJECT_TARGET STREQUAL "reference")
    add_executable(mj_reference_app
        customer_project/reference/src/main.cpp
    )

    target_link_libraries(mj_reference_app PRIVATE mj_sdk)
    target_compile_features(mj_reference_app PRIVATE cxx_std_11)

    set_target_properties(mj_reference_app PROPERTIES
        CXX_STANDARD 11
        CXX_STANDARD_REQUIRED ON
        CXX_EXTENSIONS OFF
    )
endif()

message(STATUS "SDK_HW_TARGET=${SDK_HW_TARGET} canonical=${SDK_HW_TARGET_CANONICAL}")
message(STATUS "SDK_OS_TARGET=${SDK_OS_TARGET} canonical=${SDK_OS_TARGET_CANONICAL}")
message(STATUS "SDK_PROJECT_TARGET=${SDK_PROJECT_TARGET}")
message(STATUS "SDK_CAPTURE_TARGET=${SDK_CAPTURE_TARGET}")
message(STATUS "SDK_DISPLAY_TARGET=${SDK_DISPLAY_TARGET}")
message(STATUS "SDK_CONFIG=${SDK_CONFIG_PATH}")
