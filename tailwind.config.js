/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './templates/**/*.html',
    './core/templates/**/*.html',
    './accounts/templates/**/*.html',
    './**/templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors:{
      'dark-main': '#18191a',
      'dark-second': '#242526',
      'dark-third': '#3a3b3c',
      'dark-txt': '#e4e6eb',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}