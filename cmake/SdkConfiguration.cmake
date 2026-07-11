function(sdk_resolve_configuration_path config_path output_variable)
    if(IS_ABSOLUTE "${config_path}")
        set(resolved_path "${config_path}")
    else()
        set(resolved_path "${CMAKE_CURRENT_SOURCE_DIR}/${config_path}")
    endif()

    set(${output_variable} "${resolved_path}" PARENT_SCOPE)
endfunction()

function(sdk_load_configuration yaml_file)
    if(NOT EXISTS "${yaml_file}")
        message(FATAL_ERROR "Configuration file not found: ${yaml_file}")
    endif()

    file(STRINGS "${yaml_file}" yaml_lines)

    foreach(line IN LISTS yaml_lines)
        string(REGEX REPLACE "#.*$" "" line_without_comment "${line}")
        string(STRIP "${line_without_comment}" line_trimmed)

        if(line_trimmed STREQUAL "")
            continue()
        endif()

        if(NOT line_trimmed MATCHES "^([A-Za-z_][A-Za-z0-9_]*)[ \t]*:[ \t]*(.*)$")
            message(FATAL_ERROR "Unsupported configuration line in ${yaml_file}: ${line}")
        endif()

        set(key "${CMAKE_MATCH_1}")
        set(value "${CMAKE_MATCH_2}")
        string(STRIP "${value}" value)
        string(REGEX REPLACE "^['\"]|['\"]$" "" value "${value}")

        set(yaml_value_variable "SDK_YAML_VALUE_${key}")
        set(apply_yaml_value FALSE)

        if(NOT DEFINED ${key})
            set(apply_yaml_value TRUE)
        elseif(DEFINED ${yaml_value_variable})
            if("${${key}}" STREQUAL "${${yaml_value_variable}}")
                set(apply_yaml_value TRUE)
            endif()
        else()
            get_property(cache_type CACHE "${key}" PROPERTY TYPE)
            if(NOT cache_type STREQUAL "UNINITIALIZED")
                # Migrate cache entries created by older versions of the loader.
                set(apply_yaml_value TRUE)
            endif()
        endif()

        if(apply_yaml_value)
            set(${key} "${value}" CACHE STRING "SDK configuration value from ${yaml_file}" FORCE)
        endif()

        set(${yaml_value_variable} "${value}" CACHE INTERNAL "Last YAML value for ${key}" FORCE)
    endforeach()
endfunction()

function(sdk_require_one_of variable allowed_values)
    if(NOT DEFINED ${variable})
        message(FATAL_ERROR "${variable} is not defined")
    endif()

    set(value "${${variable}}")
    list(FIND allowed_values "${value}" found_index)

    if(found_index EQUAL -1)
        string(REPLACE ";" ", " allowed_values_text "${allowed_values}")
        message(FATAL_ERROR "${variable}=${value} is not supported. Allowed values: ${allowed_values_text}")
    endif()
endfunction()

function(sdk_define_boolean_option variable description default_value)
    if(DEFINED ${variable})
        set(value "${${variable}}")
    else()
        set(value "${default_value}")
    endif()

    string(TOUPPER "${value}" value)
    if(NOT value STREQUAL "ON" AND NOT value STREQUAL "OFF")
        message(FATAL_ERROR "${variable}=${value} is not supported. Allowed values: ON, OFF")
    endif()

    set(${variable} "${value}" CACHE BOOL "${description}" FORCE)
endfunction()

function(sdk_add_existing_subdirectory subdirectory)
    if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${subdirectory}/CMakeLists.txt")
        message(FATAL_ERROR "CMake subdirectory not found: ${CMAKE_CURRENT_SOURCE_DIR}/${subdirectory}")
    endif()

    add_subdirectory("${subdirectory}")
endfunction()

function(sdk_normalize_configuration)
    set(sdk_hw_allowed vanila vanilla nvidia arm)
    set(sdk_os_allowed linux windows)
    set(sdk_project_allowed reference customer1)
    set(sdk_capture_allowed camera raw raw_file opencv ffmpeg)
    set(sdk_display_allowed hdmi raw raw_file opencv ffmpeg)

    sdk_require_one_of(SDK_HW_TARGET "${sdk_hw_allowed}")
    sdk_require_one_of(SDK_OS_TARGET "${sdk_os_allowed}")
    sdk_require_one_of(SDK_PROJECT_TARGET "${sdk_project_allowed}")
    sdk_require_one_of(SDK_CAPTURE_TARGET "${sdk_capture_allowed}")
    sdk_require_one_of(SDK_DISPLAY_TARGET "${sdk_display_allowed}")

    set(hw_canonical "${SDK_HW_TARGET}")
    if(hw_canonical STREQUAL "vanila")
        set(hw_canonical "vanilla")
    endif()

    set(os_canonical "${SDK_OS_TARGET}")
    set(capture_canonical "${SDK_CAPTURE_TARGET}")
    if(capture_canonical STREQUAL "raw")
        set(capture_canonical "raw_file")
    endif()

    set(display_canonical "${SDK_DISPLAY_TARGET}")
    if(display_canonical STREQUAL "raw")
        set(display_canonical "raw_file")
    endif()

    set(SDK_HW_TARGET_CANONICAL "${hw_canonical}" CACHE INTERNAL "Canonical HW target")
    set(SDK_OS_TARGET_CANONICAL "${os_canonical}" CACHE INTERNAL "Canonical OS target")
    set(SDK_CAPTURE_TARGET_CANONICAL "${capture_canonical}" CACHE INTERNAL "Canonical capture target")
    set(SDK_DISPLAY_TARGET_CANONICAL "${display_canonical}" CACHE INTERNAL "Canonical display target")
endfunction()
