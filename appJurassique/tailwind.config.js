/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        'gray-div': 'rgba(26, 31, 26, 1)',
        'green-l': 'rgba(0, 255, 77, 1)',
        'green-line': 'rgba(49, 190, 75, 1)',
        'green-text': 'rgba(0, 199, 43, 1)',
        'green-ext-radial': 'rgba(0, 179, 54 ,1)',
        'green-center-radial': 'rgba(0, 91, 27, 1)',
        'gray-button-hover': 'rgba(50, 50, 50, 1)',
        'gray-textfield': 'rgba(88, 88, 88, 1)'
      },
    },
  },
  
  fontFamily: {
        'nunito': ['Nunito', 'sans-serif'],
        'exo': ['Exo', 'sans-serif']
      },
  plugins: [],
}

