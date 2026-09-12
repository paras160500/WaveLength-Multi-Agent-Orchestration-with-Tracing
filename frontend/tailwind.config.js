/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "#F4F2EC",
        surface: "#FFFFFF",
        line: "#E4E1D5",
        ink: "#20231F",
        muted: "#6E6C61",
        faint: "#9B998E",
        forest: "#163A2E",
        forest2: "#1F5443",
        teal: "#2E8069",
        tealLight: "#E4F0EA",
        amber: "#C97A2B",
        amberLight: "#FBEEDD",
        rose: "#B4483A",
        roseLight: "#FBEAE7",
      },
      fontFamily: {
        sans: ["'Inter'", "sans-serif"],
      },
      boxShadow: {
        panel: "0 1px 2px rgba(32, 35, 31, 0.04), 0 8px 24px -12px rgba(32, 35, 31, 0.10)",
      },
      borderRadius: {
        xl2: "14px",
      },
    },
  },
  plugins: [],
};
