/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['class'],
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        brand: {
          50: '#f5f3ff',
          100: '#ede9fe',
          200: '#ddd6fe',
          300: '#c4b5fd',
          400: '#a78bfa',
          500: '#8b5cf6',
          600: '#7c3aed',
          700: '#6d28d9',
          800: '#5b21b6',
          900: '#4c1d95',
          neon: '#6366f1',
          accent: '#8b5cf6',
        },
        dark: {
          bg: '#080c14',
          card: '#0d1322',
          'card-hover': '#11192e',
          card2: '#0b101d',
          border: '#182238',
          'border-light': '#22304e',
          muted: '#64748b',
          text: '#94a3b8',
          heading: '#f8fafc',
        },
        trading: {
          green: '#10b981',
          'green-glow': '#10b98140',
          red: '#ef4444',
          'red-glow': '#ef444440',
          yellow: '#f59e0b',
          cyan: '#06b6d4',
          purple: '#8b5cf6',
        }
      },
      borderRadius: {
        lg: '16px',
        md: '12px',
        sm: '8px',
        xl: '20px',
        '2xl': '24px',
      },
      fontFamily: {
        sans: ['Inter', 'Outfit', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Roboto Mono', 'monospace'],
      },
      boxShadow: {
        'glow-purple': '0 0 25px -5px rgba(139, 92, 246, 0.45)',
        'glow-green': '0 0 25px -5px rgba(16, 185, 129, 0.45)',
        'glow-cyan': '0 0 25px -5px rgba(6, 182, 212, 0.45)',
        'glow-card': '0 8px 32px 0 rgba(0, 0, 0, 0.45)',
        'glow-inner': 'inset 0 1px 1px 0 rgba(255, 255, 255, 0.08)',
      },
      animation: {
        'pulse-subtle': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow-shift': 'glowShift 6s ease-in-out infinite alternate',
      },
      keyframes: {
        glowShift: {
          '0%': { filter: 'drop-shadow(0 0 8px rgba(99,102,241,0.4))' },
          '100%': { filter: 'drop-shadow(0 0 16px rgba(139,92,246,0.7))' },
        }
      }
    },
  },
  plugins: [],
}
