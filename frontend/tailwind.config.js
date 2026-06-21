/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#13211a",
        leaf: "#2f6f4e",
        tide: "#1f7a8c",
        clay: "#b85f45",
        paper: "#f7f3ea",
      },
      boxShadow: {
        soft: "0 18px 60px rgba(19, 33, 26, 0.12)",
      },
    },
  },
  plugins: [],
};
