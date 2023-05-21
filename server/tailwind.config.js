/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./web/templates/**/*.html",
    "./web/static/scripts/*.js",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: ["flowbite/plugin"],
};
