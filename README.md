Omniverse Kit App Template


📝 Feature Branch Information
This repository is based on a Feature Branch of the Omniverse Kit SDK. Feature Branches are regularly updated and best suited for testing and prototyping. For stable, production-oriented development, please use the Production Branch of the Kit SDK on NVIDIA GPU Cloud (NGC).

Omniverse Release Information

Overview
Welcome to kit-app-template, a toolkit designed for developers interested in GPU-accelerated application development within the NVIDIA Omniverse ecosystem. This repository offers streamlined tools and templates to simplify creating high-performance, OpenUSD-based desktop or cloud streaming applications using the Omniverse Kit SDK.

About Omniverse Kit SDK
The Omniverse Kit SDK enables developers to build immersive 3D applications. Key features include:

Language Support: Develop with either Python or C++, offering flexibility for various developer preferences.
OpenUSD Foundation: Utilize the robust Open Universal Scene Description (OpenUSD) for creating, manipulating, and rendering rich 3D content.
GPU Acceleration: Leverage GPU-accelerated capabilities for high-fidelity visualization and simulation.
Extensibility: Create specialized extensions that provide dynamic user interfaces, integrate with various systems, and offer direct control over OpenUSD data, making the Omniverse Kit SDK versatile for numerous applications.
Applications and Use Cases
The kit-app-template repository enables developers to create cross-platform applications (Windows and Linux) optimized for desktop use and cloud streaming. Potential use cases include designing and simulating expansive virtual environments, producing high-quality synthetic data for AI training, and building advanced tools for technical analysis and insights. Whether you're crafting engaging virtual worlds, developing comprehensive analysis tools, or creating simulations, this repository, along with the Kit SDK, provides the foundational components required to begin development.

A Deeper Understanding
The kit-app-template repository is designed to abstract complexity, jumpstarting your development with pre-configured templates, tools, and essential boilerplate. For those seeking a deeper understanding of the application and extension creation process, we have provided the following resources:

Companion Tutorial
Explore the Kit SDK Companion Tutorial: This tutorial offers detailed insights into the underlying structure and mechanisms, providing a thorough grasp of both the Kit SDK and the development process.

New Developers
For a beginner-friendly introduction to application development using the Omniverse Kit SDK, see the NVIDIA DLI course:

Beginner Tutorial
Developing an Omniverse Kit-Based Application: This course offers an accessible introduction to application development (account and login required).

These resources empower developers at all experience levels to fully utilize the kit-app-template repository and the Omniverse Kit SDK.

Table of Contents
Overview
Prerequisites and Environment Setup
Repository Structure
Quick Start
Templates
Applications
Extensions
Tools
License
Additional Resources
Contributing
Prerequisites and Environment Setup
Ensure your system is set up with the following to work with Omniverse Applications and Extensions:

Operating System: Windows 10/11 or Linux (Ubuntu 22.04 or newer)

GPU: NVIDIA RTX capable GPU (RTX 3070 or Better recommended)

Driver: Minimum and recommended - This update requires driver version >=550.54.15 (Linux) or >=551.78 (Windows). Please verify your driver versions before upgrading. Newer versions may work but are not equally validated.

Internet Access: Required for downloading the Omniverse Kit SDK, extensions, and tools.

Required Software Dependencies
Git: For version control and repository management

Git LFS: For managing large files within the repository

(Windows - C++ Only) Microsoft Visual Studio (2019 or 2022): You can install the latest version from Visual Studio Downloads. Ensure that the Desktop development with C++ workload is selected. Additional information on Windows development configuration

(Windows - C++ Only) Windows SDK: Install this alongside MSVC. You can find it as part of the Visual Studio Installer. Additional information on Windows development configuration

(Linux) build-essentials: A package that includes make and other essential tools for building applications. For Ubuntu, install with sudo apt-get install build-essential

Recommended Software
(Linux) Docker: For containerized development and deployment. Ensure non-root users have Docker permissions.

(Linux) NVIDIA Container Toolkit: For GPU-accelerated containerized development and deployment. Installation and Configuring Docker steps are required.

VSCode (or your preferred IDE): For code editing and development

Repository Structure
Directory Item	Purpose
.vscode	VS Code configuration details and helper tasks
readme-assets/	Images and additional repository documentation
templates/	Template Applications and Extensions.
tools/	Tooling settings and repository specific (local) tools
.editorconfig	EditorConfig file.
.gitattributes	Git configuration.
.gitignore	Git configuration.
LICENSE	License for the repo.
README.md	Project information.
premake5.lua	Build configuration - such as what apps to build.
repo.bat	Windows repo tool entry point.
repo.sh	Linux repo tool entry point.
repo.toml	Top level configuration of repo tools.
repo_tools.toml	Setup of local, repository specific tools
Quick Start
