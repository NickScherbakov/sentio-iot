# Sentio IoT Landing Page

This directory contains the marketing landing page for Sentio IoT.

## Overview

A modern, professional single-page website showcasing Sentio IoT's features, capabilities, and use cases.

## Features

- **Single-file solution**: Everything in one `index.html` file
- **Modern design**: Dark-themed with gradient backgrounds and smooth animations
- **Fully responsive**: Optimized for mobile, tablet, and desktop viewing
- **No build required**: Uses CDN resources (Tailwind CSS, FontAwesome)
- **No external images**: Uses CSS gradients and FontAwesome icons

## Usage

### Local Development

Simply open the `index.html` file in any modern web browser:

```bash
# Option 1: Direct file open
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows

# Option 2: Local HTTP server
cd website
python3 -m http.server 8000
# Then visit http://localhost:8000
```

### Deployment

The landing page can be deployed to any static hosting service:

- **GitHub Pages**: Push to `gh-pages` branch
- **Netlify**: Drag and drop the `website` folder
- **Vercel**: Deploy the `website` directory
- **AWS S3**: Upload `index.html` to an S3 bucket with static website hosting
- **Cloudflare Pages**: Connect your repository and set build directory to `website`

## Content Sections

1. **Hero Section**: Main headline with call-to-action
2. **Features Grid**: Four key features (Unified Observability, AI-Powered Analytics, Horizontal Scalability, Modern Dashboard)
3. **Tech Stack**: Powered by VictoriaMetrics, Loki, Tempo, FastAPI, and React
4. **Use Cases**: Smart Home, Industrial IoT, Fleet Management
5. **CTA Section**: Secondary call-to-action with GitHub and documentation links
6. **Footer**: Copyright, license info, and community links

## Technology

- **Tailwind CSS** (via CDN) - Utility-first CSS framework
- **FontAwesome** (via CDN) - Icon library
- **Vanilla JavaScript** - Minimal JS for dynamic copyright year

## Customization

To customize the landing page:

1. Edit colors in the Tailwind config section (lines 15-26)
2. Modify content directly in the HTML
3. Adjust gradients in the `<style>` section (lines 28-50)
4. Update links to point to your repository

## Browser Support

Works in all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

This landing page is part of the Sentio IoT project and is licensed under the MIT License.
