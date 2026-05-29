/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#EEEDFE', 100: '#CECBF6', 400: '#7F77DD',
          600: '#534AB7', 800: '#3C3489', 900: '#26215C',
        },
        accent: { 50: '#E1F5EE', 400: '#1D9E75', 600: '#0F6E56' },
        warm: { 50: '#FAEEDA', 400: '#EF9F27', 600: '#BA7517' }
      },
      fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] }
    },
  },
  plugins: [],
}
