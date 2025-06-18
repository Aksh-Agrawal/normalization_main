// install-tailwind.js
const { execSync } = require("child_process");

console.log("Installing Tailwind CSS and dependencies...");
try {
  execSync(
    "npm install -D tailwindcss@latest postcss@latest autoprefixer@latest",
    { stdio: "inherit" }
  );
  console.log("Dependencies installed successfully!");

  console.log("Initializing Tailwind configuration...");
  execSync("npx tailwindcss init -p", { stdio: "inherit" });
  console.log("Tailwind configuration created!");

  console.log("All done! You can now use Tailwind CSS in your project.");
  console.log("Remember to:");
  console.log("1. Update your CSS file with Tailwind directives");
  console.log("2. Configure content paths in tailwind.config.js");
} catch (error) {
  console.error("An error occurred:", error);
}
