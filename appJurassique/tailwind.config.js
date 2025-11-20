/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./templates/*.html'],
  theme: {
    extend: {
      dropShadow: {
        'button': '0 0 2px rgba(0, 255, 77, 1)'
      },
      colors: {
        'green-button': 'rgba(0, 255, 77, 1)',
        'green-button-hover': 'rgba(0, 255, 77, 0.8)',
      },
      fontFamily: {
        'nunito': ['Nunito', 'sans-serif'],
        'exo': ['Exo', 'sans-serif']
      },
    },
  },
  plugins: [],
}

