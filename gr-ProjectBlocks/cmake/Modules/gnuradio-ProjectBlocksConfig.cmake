find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_PROJECTBLOCKS gnuradio-ProjectBlocks)

FIND_PATH(
    GR_PROJECTBLOCKS_INCLUDE_DIRS
    NAMES gnuradio/ProjectBlocks/api.h
    HINTS $ENV{PROJECTBLOCKS_DIR}/include
        ${PC_PROJECTBLOCKS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_PROJECTBLOCKS_LIBRARIES
    NAMES gnuradio-ProjectBlocks
    HINTS $ENV{PROJECTBLOCKS_DIR}/lib
        ${PC_PROJECTBLOCKS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-ProjectBlocksTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_PROJECTBLOCKS DEFAULT_MSG GR_PROJECTBLOCKS_LIBRARIES GR_PROJECTBLOCKS_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_PROJECTBLOCKS_LIBRARIES GR_PROJECTBLOCKS_INCLUDE_DIRS)
