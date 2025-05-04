/** @type {import('next-i18next').UserConfig} */
module.exports = {
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ar'],
    localeDetection: false, // Disable automatic locale detection based on browser preferences
  },
  // Optionally, specify where your locale files are located
  // localePath: typeof window === 'undefined' ? require('path').resolve('./public/locales') : '/locales',
  // reloadOnPrerender: process.env.NODE_ENV === 'development',
};

