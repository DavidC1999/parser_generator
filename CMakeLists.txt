cmake_minimum_required(VERSION 3.22)
project(parser_generator C)

set(CMAKE_C_STANDARD 23)

include(FetchContent)

# Fetch the PCRE library
FetchContent_Declare(
        pcre2
        GIT_REPOSITORY https://github.com/PCRE2Project/pcre2.git
        GIT_TAG        pcre2-10.45  # You can specify a specific tag or branch
)

FetchContent_MakeAvailable(pcre2)

execute_process(COMMAND python3 ${CMAKE_SOURCE_DIR}/generator/generate.py ${CMAKE_SOURCE_DIR})

add_executable(parser_generator
        main.c
        tokenizer.c
        tokenizer.h
        memory_arena.h
        memory_arena.c
        parser.c
        parser.h
        linked_list.c
        linked_list.h)

target_link_libraries(parser_generator pcre)