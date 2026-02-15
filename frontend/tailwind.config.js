/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Primary Brand Colors - Darker Purple Theme
        primary: {
          DEFAULT: '#6366F1',
          50: '#EEEEFF',
          100: '#E0E7FF',
          200: '#C7D2FE',
          300: '#A5B4FC',
          400: '#818CF8',
          500: '#6366F1',
          600: '#4F46E5',
          700: '#4338CA',
          800: '#3730A3',
          900: '#312E81',
        },
        // Neutral Colors - Very Dark Theme
        background: '#06060A',
        surface: '#0F0F15',
        'surface-light': '#16161E',
        border: '#1F1F28',
        // Semantic Colors for Risk Levels
        success: {
          DEFAULT: '#10B981',
          light: '#D1FAE5',
          dark: '#047857',
        },
        warning: {
          DEFAULT: '#F59E0B',
          light: '#FEF3C7',
          dark: '#D97706',
        },
        danger: {
          DEFAULT: '#EF4444',
          light: '#FEE2E2',
          dark: '#DC2626',
        },
        info: {
          DEFAULT: '#3B82F6',
          light: '#DBEAFE',
          dark: '#1D4ED8',
        },
        // Accent Colors
        accent: {
          purple: '#6366F1',
          cyan: '#06B6D4',
        },
        // Text Colors - Light on Dark
        text: {
          primary: '#F1F5F9',
          secondary: '#CBD5E1',
          muted: '#64748B',
        },
        // Glassmorphism
        glass: {
          DEFAULT: 'rgba(255, 255, 255, 0.03)',
          light: 'rgba(255, 255, 255, 0.05)',
          border: 'rgba(255, 255, 255, 0.08)',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.4)',
        'glass-lg': '0 12px 40px 0 rgba(0, 0, 0, 0.5)',
        'inner-glass': 'inset 0 1px 0 0 rgba(255, 255, 255, 0.05)',
      },
      backdropBlur: {
        'xs': '2px',
        'glass': '16px',
      },
    },
  },
  plugins: [],
}
