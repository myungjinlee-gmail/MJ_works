target_sources(mj_sdk PRIVATE
    sdk_api.cpp
)

sdk_add_existing_subdirectory("${SDK_HW_TARGET_CANONICAL}")
