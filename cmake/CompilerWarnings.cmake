function(enable_compiler_warnings target)
    if(NOT TARGET "${target}")
        message(FATAL_ERROR "Cannot enable compiler warnings for unknown target: ${target}")
    endif()

    if(MSVC)
        target_compile_options("${target}" PRIVATE /W4 /WX /permissive-)
    elseif(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        target_compile_options(
            "${target}"
            PRIVATE
                -Wall
                -Wextra
                -Wpedantic
                -Werror
                -Warray-bounds
                -Wconversion
                -Wimplicit-fallthrough
                -Wparentheses
                -Wreorder
                -Wsign-compare
                -Wsign-conversion
                -Wtype-limits
        )

        if(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
            target_compile_options(
                "${target}"
                PRIVATE
                    -Wtautological-compare
                    -Wtautological-constant-compare
                    -Wunsequenced
            )
        else()
            target_compile_options("${target}" PRIVATE -Wsequence-point)
        endif()
    else()
        message(WARNING "Compiler warning policy is not defined for ${CMAKE_CXX_COMPILER_ID}")
    endif()
endfunction()
