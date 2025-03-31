# Changelog

All notable changes to PyVueBot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-03-31

### Added
- Dynamic template variable substitution system using `{{ variable_name }}` syntax
- Interactive setup wizard for project creation
- Environment variables configuration during project setup
- Support for .env.example files in templates
- Comprehensive webhook management commands:
  - `webhook set` - Configure Telegram bot webhooks
  - `webhook info` - Display webhook status information
  - `webhook delete` - Remove existing webhooks
- Force option (`-f`, `--force`) to overwrite existing directories
- Version command and flags (`-v`, `--version`)
- Modular CLI architecture for better maintainability

### Changed
- Refactored CLI structure into modular components
- Enhanced project configuration with additional metadata
- Improved error handling for project creation
- Updated documentation with new features and options

### Fixed
- Directory existence checking before project creation
- Environment variable handling with proper escaping

## [0.1.0] - 2025-03-30

### Added
- Initial release of PyVueBot
- Project scaffolding with task_manager template
- Basic CLI commands for project management:
  - `init` - Create new project 
  - `install` - Install dependencies
  - `dev` - Run development server
  - `build` - Build for production
  - `deploy` - Deploy to Vercel
- Template-based project structure generation
- Supabase database integration
- Telegram Mini App boilerplate with Vue.js
- FastAPI backend integration
- Vercel deployment configuration