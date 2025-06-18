// tailwind-examples.js

/**
 * This file contains examples of Tailwind CSS utility classes for common UI patterns.
 * These aren't functional components - they're just examples to copy from.
 */

// --- Form Elements ---

// Text Input
const inputExample = `<input 
  type="text" 
  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500" 
  placeholder="Enter text..."
/>`;

// Button Variants
const buttonExamples = {
  primary: `<button className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2">
  Submit
</button>`,
  secondary: `<button className="px-4 py-2 bg-gray-100 text-gray-800 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2">
  Cancel
</button>`,
  danger: `<button className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2">
  Delete
</button>`,
};

// --- Layout Patterns ---

// Simple Card
const cardExample = `<div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow duration-300">
  <h3 className="text-lg font-medium text-gray-900">Card Title</h3>
  <p className="mt-2 text-sm text-gray-500">This is a simple card example using Tailwind CSS utility classes.</p>
  <div className="mt-4">
    <a href="#" className="text-primary-600 hover:text-primary-800 font-medium">Learn more →</a>
  </div>
</div>`;

// Responsive Grid
const gridExample = `<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <div>Column 1</div>
  <div>Column 2</div>
  <div>Column 3</div>
</div>`;

// --- Component Examples ---

// Alert/Notification
const alertExamples = {
  success: `<div className="bg-green-50 border-l-4 border-green-400 p-4">
  <div className="flex items-center">
    <div className="flex-shrink-0">
      <!-- Success icon -->
    </div>
    <div className="ml-3">
      <p className="text-sm text-green-700">
        Successfully saved your changes!
      </p>
    </div>
  </div>
</div>`,
  error: `<div className="bg-red-50 border-l-4 border-red-400 p-4">
  <div className="flex items-center">
    <div className="flex-shrink-0">
      <!-- Error icon -->
    </div>
    <div className="ml-3">
      <p className="text-sm text-red-700">
        There was an error processing your request.
      </p>
    </div>
  </div>
</div>`,
};

// Loading Spinner
const loadingSpinner = `<div className="flex justify-center items-center">
  <div className="animate-spin rounded-full h-6 w-6 border-4 border-gray-200 border-t-primary-600"></div>
  <span className="ml-2">Loading...</span>
</div>`;

// Navigation
const navExample = `<nav className="bg-white shadow">
  <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
    <div className="flex justify-between h-16">
      <div className="flex">
        <div className="flex-shrink-0 flex items-center">
          <img className="h-8 w-auto" src="/logo.svg" alt="Logo" />
        </div>
        <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
          <a href="#" className="border-primary-500 text-gray-900 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
            Home
          </a>
          <a href="#" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
            Features
          </a>
          <a href="#" className="border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
            About
          </a>
        </div>
      </div>
      <div className="hidden sm:ml-6 sm:flex sm:items-center">
        <button className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700">
          Sign In
        </button>
      </div>
    </div>
  </div>
</nav>`;
