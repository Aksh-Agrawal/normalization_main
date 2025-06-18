# Tailwind CSS Setup for Coding Profile Analyzer

This document provides instructions on how to configure and use Tailwind CSS in this project.

## What is Tailwind CSS?

Tailwind CSS is a utility-first CSS framework that allows you to build custom designs without leaving your HTML. Instead of predefined components, Tailwind provides low-level utility classes that let you build completely custom designs.

## Setup Instructions

We've already configured the project with Tailwind CSS. To get started:

1. Install dependencies:

```bash
npm install
```

2. Run Tailwind CSS setup (if needed):

```bash
npm run setup-tailwind
```

3. Start the development server:

```bash
npm run dev
```

## Using Tailwind CSS

- Use utility classes directly in your JSX components
- Example: `className="flex items-center justify-between p-4 bg-white rounded-lg shadow"`

## Customizing Tailwind

To customize Tailwind's default configuration:

1. Edit `tailwind.config.js` to add custom colors, fonts, etc.
2. Run `npm run build` to apply changes

## Tailwind Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Tailwind CSS Cheat Sheet](https://nerdcave.com/tailwind-cheat-sheet)
- [Tailwind UI Components](https://tailwindui.com/)

## Common Patterns

### Layouts

```jsx
<div className="container mx-auto px-4">
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {/* Content */}
  </div>
</div>
```

### Cards

```jsx
<div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
  <h3 className="text-xl font-semibold text-gray-800">Card Title</h3>
  <p className="text-gray-600 mt-2">Card content goes here</p>
</div>
```

### Buttons

```jsx
<button className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700">
  Click Me
</button>
```
