project(main)

cmake_minimum_required(VERSION 2.8)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${PROJECT_SOURCE_DIR}/cmake")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++0x")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
INCLUDE_DIRECTORIES(include)

file(GLOB SOURCES "src/*.cpp")
file(GLOB HEADERS "include/*.h")
add_executable(${PROJECT_NAME} ${SOURCES} )

find_package(SDL2 REQUIRED)
#find_package(SDL2_image REQUIRED >=2.0.0)
#find_package(OpenGL REQUIRED)
include_directories(${PROJECT_NAME} ${SDL2_INCLUDE_DIR} )#${SDL2_IMAGE_INCLUDE_DIR} ${OPENGL_INCLUDE_DIR})
target_link_libraries(${PROJECT_NAME} ${SDL2_LIBRARY} )#${SDL2_IMAGE_LIBRARY} ${OPENGL_LIBRARIES})  