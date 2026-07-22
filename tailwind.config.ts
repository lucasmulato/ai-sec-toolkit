import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./tests/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      // Optional: Add custom colors or fonts here if needed
    },
  },
  plugins: [],
};
export default config;