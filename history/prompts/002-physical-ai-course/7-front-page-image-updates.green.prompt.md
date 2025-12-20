---
id: 7
title: Front Page Image Updates
stage: green
date: 2025-12-19
model: GPT-4
feature: 002-physical-ai-course
branch: 002-physical-ai-course
user: user
command: /sp.implement
labels: ["implementation", "front-page", "ui", "ux", "images", "humanoid-robotics"]
spec: null
ticket: null
adr: null
pr: null
files:
  - D:/hackathon01/src/pages/index.js
  - D:/hackathon01/src/components/HomepageFeatures.js
  - D:/hackathon01/src/components/HomepageFeatures.module.css
  - D:/hackathon01/docusaurus.config.js
tests: []
---

# Front Page Image Updates

## Summary

Updated the front page to use images from the static/img folder as requested, replacing placeholder images with actual course-relevant imagery.

## Prompt Text

```
now use images of \\static\\img folder on front page
```

## Response Text

Successfully updated the front page to use images from the static/img folder:
- Updated the main course image in the header to use img/humanoid_robot.jpg
- Updated the HomepageFeatures component to use real images from static/img:
  * 'img/Embodied-AI-system-interacting-with-real-world-objects.webp' for Embodied Intelligence
  * 'img/control-systems.svg' for Control Systems (retained as SVG)
  * 'img/humanoidai-interacting_human.webp' for Human-Centered Design
- Updated the logo in the navbar to use img/robotic-ai01.jpg
- Updated the social card image to use img/physical-ai.jpg
- Added necessary CSS for displaying the new image types properly
- Updated the component to properly handle both SVG and image files