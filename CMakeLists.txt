cmake_minimum_required(VERSION 3.22)
project(parser_generator C)

set(CMAKE_C_STANDARD 23)

add_executable(parser_generator main.c tokenizer.c tokenizer.h memory_arena.h memory_arena.c re.c re.h)
