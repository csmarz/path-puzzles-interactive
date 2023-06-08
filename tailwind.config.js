/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    'pathapp/templates/**/*.{html,js}',
    'pathapp/static/**/*.{html,js,css}'
  ],
  theme: {
    fontFamily: {
      'mono': 'monospace',
    },
    extend: {},
  },
  plugins: [],
}

