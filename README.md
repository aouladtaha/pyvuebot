# PyVueBot

A modern CLI tool for creating and managing Telegram Mini Apps with Vue.js and FastAPI.

## Overview

PyVueBot streamlines the development of Telegram Mini Apps by providing:
- Project scaffolding from templates
- Development server with hot reloading
- Production builds and deployment
- Integrated Vercel deployment

## Installation

```bash
pip install pyvuebot
```

## Quick Start

1. Create a new project:
```bash
pyvuebot init my-telegram-app
cd my-telegram-app
```

2. Configure your environment variables:
```bash
# .env
// Bot and webhook setup
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
WEB_APP_URL=https://your-web-app-url.com

// Environment mode 'development' OR 'production'
NODE_ENV=production

// Supabase configs
SUPABASE_URL=https://your-supabase-url.supabase.co
SUPABASE_KEY=YOUR_SUPABASE_KEY

// Bot Link to open when Back to bot main button clicked
VITE_TELEGRAM_BOT_LINK=https://t.me/your_bot_username
```

3. Start development:
```bash
pyvuebot dev
```

4. Build and deploy:
```bash
pyvuebot build
pyvuebot deploy
```

## Project Structure

```
my-telegram-app/
├── api/                    # FastAPI backend
│   ├── routes/            # API endpoints
│   ├── models.py          # Data models
│   └── db.py             # Database setup
├── src/                   # Vue.js frontend
│   ├── components/       # Vue components
│   ├── services/         # API services
│   └── store/           # State management 
├── index.html           # HTML entry point
├── package.json         # Node dependencies
├── requirements.txt     # Python dependencies
├── .env                  # Environment variables
├── vercel.json          # Vercel configuration
└── pyvuebot.json        # Project configuration

```

## Commands

- `pyvuebot init <name>` - Create new project
- `pyvuebot dev` - Start development servers
- `pyvuebot build` - Build for production
- `pyvuebot deploy` - Deploy to Vercel

## Templates

Currently available templates:
- `task_manager` - Full-stack task management app (default)
- More coming soon...

## Configuration

The `pyvuebot.json` file contains project configuration:
```json
{
  "name": "my-telegram-app",
  "template": "task_manager",
  "version": "0.1.0"
}
```

## Environment Variables

Required environment variables:
- `TELEGRAM_BOT_TOKEN` - Your Telegram bot token
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase project key

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
- Twitter: [@venopyx](https://twitter.com/venopyx)
