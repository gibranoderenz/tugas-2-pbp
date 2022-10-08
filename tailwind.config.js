/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./todolist/**/*.{html,js}"],
  extend: {},
  plugins: [
    require("@tailwindcss/typography"),
    require("@tailwindcss/forms"),
    require("@tailwindcss/line-clamp"),
    require("@tailwindcss/aspect-ratio"),
  ],
};
