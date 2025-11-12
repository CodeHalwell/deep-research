# Deep Research Frontend

A modern, type-safe React/Next.js/TypeScript frontend for the Deep Research Workflow System.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ (recommended 20+)
- npm or yarn or pnpm

### Installation

```bash
# Install dependencies
npm install

# Set up environment variables (if needed)
cp .env.example .env.local

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### API Configuration

The frontend connects to the backend API server (default: `http://localhost:8000`). You can configure this:

1. **In the UI**: Go to "Submit Research" tab and update the API Server URL
2. **Environment Variables**: Create a `.env.local` file with:
   ```
   NEXT_PUBLIC_API_URL=http://your-api-server:8000
   ```

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js app directory (pages)
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home/Submit Research page
│   ├── monitor/           # Monitor workflow page
│   ├── history/           # View workflow history page
│   ├── about/             # About system page
│   └── globals.css        # Global styles
├── components/            # Reusable React components
│   ├── ui/               # Base UI components (button, card, input, etc.)
│   ├── navigation.tsx    # Top navigation bar
│   ├── theme-provider.tsx # Dark mode support
│   └── root-layout-client.tsx # Client layout wrapper
├── lib/                   # Utility functions and API client
│   ├── api.ts            # API client
│   └── utils.ts          # Utility functions
├── hooks/                 # Custom React hooks
├── public/               # Static assets
└── package.json          # Dependencies and scripts
```

## 🎨 Features

### Pages

1. **Submit Research** (`/`)
   - Submit new research topics
   - API connection status indicator
   - Quick example topics
   - Real-time validation

2. **Monitor** (`/monitor`)
   - Track workflow progress
   - View statistics and metrics
   - Download completed reports
   - Auto-refresh capability
   - Check workflow status

3. **History** (`/history`)
   - View all past workflows
   - Search and filter workflows
   - Quick access to monitor workflows
   - Workflow statistics

4. **About** (`/about`)
   - System information and features
   - Architecture overview
   - Technology stack
   - Research workflow explanation

### UI Components

- **Button**: Customizable button with loading state
- **Card**: Container component with header/content/footer
- **Input**: Text input with validation styling
- **Textarea**: Multi-line text input
- **Badge**: Status and label display
- **Tabs**: Tab navigation
- **Progress**: Progress bar visualization
- **Alert**: Alert/notification display
- **Label**: Form labels

### Theming

- **Dark Mode**: Toggle dark/light theme (persisted to localStorage)
- **Tailwind CSS**: Utility-first CSS framework
- **Custom Color Scheme**: HSL-based color variables for easy customization

## 🔧 Development

### Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm start        # Start production server
npm run lint     # Run ESLint
```

### Building for Production

```bash
npm run build
npm start
```

### Code Style

- **TypeScript**: Full type safety
- **ESLint**: Code quality and consistency
- **Prettier** (optional): Code formatting

## 📡 API Integration

The frontend communicates with the backend API at `/api` endpoints:

- `POST /workflows` - Submit a new workflow
- `GET /workflows/{id}` - Get workflow status
- `GET /workflows/{id}/result` - Get workflow results
- `GET /workflows/{id}/statistics` - Get workflow statistics
- `GET /workflows/{id}/report` - Download report (HTML/PDF)
- `GET /workflows` - List all workflows
- `GET /health` - Health check

See `lib/api.ts` for the API client implementation.

## 🎯 Customization

### Changing Colors

Edit `app/globals.css` to modify CSS variables:

```css
--primary: 262 80% 50%;          /* Primary brand color */
--secondary: 263 70% 50%;        /* Secondary accent */
--destructive: 0 84.2% 60.2%;   /* Error/destructive actions */
```

### Modifying Tailwind Config

Edit `tailwind.config.ts` to customize:
- Color schemes
- Typography
- Spacing
- Responsive breakpoints

### API Base URL

Update in:
- `lib/api.ts`: `const baseURL = "http://localhost:8000"`
- Or use environment variable: `NEXT_PUBLIC_API_URL`

## 🚢 Deployment

### Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

### Docker

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

### Environment Variables for Production

```env
NEXT_PUBLIC_API_URL=https://your-api-server.com
```

## 📦 Dependencies

### Production
- **React 18**: UI library
- **Next.js 15**: React framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Axios**: HTTP client
- **Lucide React**: Icons
- **date-fns**: Date utilities

### Development
- **ESLint**: Code quality
- **TypeScript**: Type checking

## 🐛 Troubleshooting

### API Connection Issues

1. Check if API server is running: `http://localhost:8000/health`
2. Update API URL in the UI
3. Check CORS settings in backend
4. Verify network connectivity

### Build Issues

```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Try building again
npm run build
```

### Performance

- Use React DevTools to profile components
- Check Lighthouse scores in browser DevTools
- Optimize images in `/public` directory
- Enable static generation for pages when possible

## 📝 Notes

- The frontend automatically persists API URL to localStorage
- Workflow IDs are automatically copied to clipboard on submission
- Auto-refresh is available on the Monitor page
- Dark mode preference is saved to localStorage

## 🤝 Contributing

Contributions are welcome! Please:

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

[Add your license]

## 📞 Support

For issues or questions:
1. Check the GitHub issues
2. Review the main project documentation
3. Check the API server logs
4. Contact the development team

---

**Happy researching! 🔬**
