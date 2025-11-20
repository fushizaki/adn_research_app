/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        'gray-div': 'rgba(26, 31, 26, 1)',
        'green-l': 'rgba(0, 255, 77, 1)'
      },
    },
  },
  
  fontFamily: {
        'nunito': ['Nunito', 'sans-serif'],
        'exo': ['Exo', 'sans-serif']
      },
  plugins: [],
}

