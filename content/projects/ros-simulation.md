---
{
  "slug": "ros-simulation",
  "template": "general",
  "title": "Autonomous Indoor Robot",
  "category": "ROS 2 simulation",
  "subtitle": "Indoor navigation and AprilTag detection | March–May 2026",
  "role": "ROS 2 system integration, localization, perception, and mission sequencing",
  "summary": "An autonomous simulated robot integrating mecanum wheel odometry, indoor navigation, and AprilTag detection.",
  "metrics": [["ROS 2", "robotics platform"], ["3", "AprilTag targets"], ["<0.1 m", "reported pose accuracy"]],
  "tags": ["ROS 2", "AMCL", "Nav2", "LiDAR", "AprilTags", "TF"],
  "images": [{"file": "ros-system.png", "caption": "System overview based on the resume description; illustrative diagram, not a simulation screenshot."}],
  "source": "Manan_Robotics_Resume 9_3_26.pdf, Projects",
  "review_status": "Seeded from the robotics resume. Project narrative and screenshots pending owner review."
}
---
## Objective
Build an autonomous ROS 2 system that navigates a simulated indoor environment and detects three AprilTag markers. The project ran from March to May 2026.

## My contribution
I integrated mecanum wheel odometry, AMCL localization, and Nav2 path planning. The sensor fusion pipeline combined LiDAR-based localization using AMCL/slam toolbox with camera-based AprilTag detection and TF chain composition.

## Mission execution
I implemented a multi-threaded mission sequencer with dynamic scan-skipping based on live TF state. The resume reports sub-0.1 m marker pose accuracy in the map frame.
