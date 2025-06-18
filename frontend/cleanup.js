/**
 * This script helps clean up duplicate files in the project
 * Run with: node cleanup.js
 */

const fs = require("fs");
const path = require("path");

// Function to check if two files have identical content
const areFilesIdentical = (file1, file2) => {
  try {
    const content1 = fs.readFileSync(file1, "utf8");
    const content2 = fs.readFileSync(file2, "utf8");
    return content1 === content2;
  } catch (error) {
    console.error(`Error comparing files ${file1} and ${file2}:`, error);
    return false;
  }
};

// Check for duplicates (.js and .jsx versions of the same component)
const checkForDuplicates = (dir) => {
  const files = fs.readdirSync(dir);

  // Group files by their base name (without extension)
  const fileGroups = {};

  files.forEach((file) => {
    if (fs.statSync(path.join(dir, file)).isDirectory()) {
      // Recursively check subdirectories
      checkForDuplicates(path.join(dir, file));
      return;
    }

    const baseName = path.basename(file, path.extname(file));
    if (!fileGroups[baseName]) {
      fileGroups[baseName] = [];
    }
    fileGroups[baseName].push(file);
  });

  // Check for duplicates in each group
  Object.keys(fileGroups).forEach((baseName) => {
    const group = fileGroups[baseName];
    if (group.length > 1) {
      console.log(`Found potential duplicates for ${baseName} in ${dir}:`);
      group.forEach((file) => console.log(`  - ${file}`));

      // Check if they are identical
      for (let i = 0; i < group.length - 1; i++) {
        for (let j = i + 1; j < group.length; j++) {
          const file1 = path.join(dir, group[i]);
          const file2 = path.join(dir, group[j]);

          const identical = areFilesIdentical(file1, file2);
          console.log(
            `  ${group[i]} and ${group[j]} are ${
              identical ? "identical" : "different"
            }`
          );
        }
      }
      console.log("");
    }
  });
};

const rootDir = path.join(__dirname, "src");
console.log("Checking for duplicate files...");
checkForDuplicates(rootDir);
console.log("Done!");
