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
        'gray-div': 'rgba(26, 31, 26, 1)',
        'green-text': 'rgba(0, 199, 43, 1)',
        'green-button-menu': 'rgba(36, 98, 20, 1)',
        'green-button-menu-hover': 'rgba(36, 98, 20, 0.8)',
        'gray-textfield': 'rgba(88, 88, 88, 1)',
      },
      fontFamily: {
        'nunito': ['Nunito', 'sans-serif'],
        'exo': ['Exo', 'sans-serif']
      },
    },
  },
  plugins: [],
}

