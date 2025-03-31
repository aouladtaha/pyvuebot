# PyVueBot

<img src="https://raw.githubusercontent.com/venopyX/pyvuebot/refs/heads/main/pyvuebot.png" alt="PyVueBot Logo" style="max-height: 300px;"/>

A modern CLI tool for creating and managing Telegram Mini Apps with Vue.js and FastAPI.

## Overview

PyVueBot streamlines the development of Telegram Mini Apps by providing:

- Project scaffolding from templates with variable substitution
- Interactive setup wizard for easy configuration
- Development server with hot reloading
- Production builds and deployment
- Integrated Telegram webhook management
- Vercel deployment support

---

## Installation

```bash
pip install pyvuebot
```

## Quick Start

1. Create a new project:

```bash
pyvuebot init my-telegram-app
```

2. Install dependencies:

```bash
cd my-telegram-app
pyvuebot install
```

3. Start development:

```bash
pyvuebot dev
```

4. Configure your webhook:

```bash
pyvuebot webhook set
```

5. Build and deploy:

```bash
pyvuebot build
pyvuebot deploy
```

---

## Command Reference

### Project Management

- `pyvuebot init [NAME]` - Create a new project

  - `--template` - Specify a template (default: task_manager)
  - `--description` - Project description
  - `--yes, -y` - Skip interactive prompts and use defaults
  - `--force, -f` - Override existing directory

- `pyvuebot install` - Install dependencies
- `pyvuebot dev` - Start development servers
- `pyvuebot build` - Build for production
- `pyvuebot deploy` - Deploy to Vercel

### Webhook Management

- `pyvuebot webhook set` - Set up a Telegram bot webhook

  - `--token` - Telegram bot token
  - `--url` - Web app URL
  - `--path` - Custom webhook path

- `pyvuebot webhook info` - Check webhook status

  - `--token` - Telegram bot token

- `pyvuebot webhook delete` - Delete webhook
  - `--token` - Telegram bot token
  - `--drop-pending` - Drop pending updates

---

## Templates

Currently available templates:

- `task_manager` - Full-stack task management app (default)
- More coming soon...

## Project Structure

```
my-telegram-app/
├── api/                    # FastAPI backend
│   ├── routes/             # API endpoints
│   ├── models.py           # Data models
│   └── db.py               # Database setup
├── src/                    # Vue.js frontend
│   ├── components/         # Vue components
│   ├── services/           # API services
│   └── store/              # State management
├── index.html              # HTML entry point
├── package.json            # Node dependencies
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── .env.example            # Environment variables template
├── vercel.json             # Vercel configuration
└── pyvuebot.json           # Project configuration
```

---

## Configuration

The `pyvuebot.json` file contains project configuration:

```json
{
  "name": "my-telegram-app",
  "template": "task_manager",
  "description": "My Telegram Mini App",
  "version": "0.1.0",
  "created_at": "2023-03-31T01:53:14.539642"
}
```

## Dynamic Template Variables

Templates can use variables in the format `{{ variable_name }}` which will be replaced during project creation:

- `{{ project_name }}` - Project name
- `{{ project_description }}` - Project description
- `{{ creation_date }}` - Creation date (YYYY-MM-DD)
- `{{ creation_year }}` - Creation year
- `{{ template_name }}` - Template name

## Environment Variables

Required environment variables:

- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
- `WEB_APP_URL` - URL where your app is deployed
- `SUPABASE_URL` - Supabase project URL (if using Supabase)
- `SUPABASE_KEY` - Supabase project key (if using Supabase)
- `VITE_TELEGRAM_BOT_LINK` - Link to your Telegram bot

---

## Star the Repository

If you find PyVueBot useful, please consider giving it a star on GitHub! Your support helps the project grow.

[![GitHub Repo stars](https://img.shields.io/github/stars/venopyx/pyvuebot?style=social)](https://github.com/venopyx/pyvuebot)

```bash
# Or clone and star through GitHub CLI
gh repo clone venopyx/pyvuebot
gh repo star venopyx/pyvuebot
```

---
## Development

To contribute to PyVueBot:

1. Clone the repository:

```bash
git clone https://github.com/venopyx/pyvuebot.git
cd pyvuebot
```

2. Install dependencies:

```bash
poetry install
```

3. Create a new branch:

```bash
git checkout -b feature/your-feature
```

4. Make your changes and submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details

## Author

- Gemechis Chala ([@venopyx](https://github.com/venopyx))
- Email: venopyx@gmail.com

## Support

- GitHub Issues: [Report bugs](https://github.com/venopyx/pyvuebot/issues)
- Telegram: [@venopyx](https://t.me/venopyx)
- Twitter: [@venopyx](https://twitter.com/venopyx)
