# Game Recaps Website

A simple static website to display game recaps, deployed on Cloudflare Pages.

## Features

- List all game recaps with team names and dates
- View individual game recaps
- Responsive design for all devices

## Deployment to Cloudflare Pages

1. Push this repository to GitHub
2. Go to [Cloudflare Pages](https://pages.cloudflare.com/)
3. Click on "Create a project"
4. Select your GitHub repository
5. In the build settings:
   - Framework preset: None
   - Build command: (leave empty)
   - Build output directory: (leave empty)
6. Click "Save and Deploy"

## Development

To test locally:

1. Install [Wrangler](https://developers.cloudflare.com/workers/wrangler/install-and-update/):
   ```bash
   npm install -g wrangler
   ```

2. Start the local development server:
   ```bash
   wrangler pages dev
   ```

## Project Structure

- `index.html` - Main page that lists all game recaps
- `_worker.js` - Cloudflare Worker for handling API requests
- `*.txt` - Game recap files
