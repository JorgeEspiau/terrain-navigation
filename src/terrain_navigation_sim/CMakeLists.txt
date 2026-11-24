cmake_minimum_required(VERSION 3.8)
project(terrain_navigation_sim)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)

install(DIRECTORY launch DESTINATION share/${PROJECT_NAME})
install(FILES
  ../project_gazebo/config/world.yaml
  ../project_gazebo/config/world_swarm.yaml
  ../project_gazebo/config/config.yaml
  ../project_gazebo/config/ground_truth_fortress.yaml
  ../project_gazebo/config/pid_speed_controller.yaml
  ../project_gazebo/config/pid_speed_controller_humble.yaml
  DESTINATION share/${PROJECT_NAME}/config
)
install(PROGRAMS ../project_gazebo/utils/keyboard_teleoperation.py
  DESTINATION lib/${PROJECT_NAME}
)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
