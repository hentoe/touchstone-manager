/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./touchstone_manager/templates/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [
      require('@tailwindcss/forms'),
  ],
}
