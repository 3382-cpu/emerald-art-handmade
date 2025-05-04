import {getRequestConfig} from 'next-intl/server';
 
// Can be imported from a shared config
const locales = ['en', 'ar'];
 
export default getRequestConfig(async ({locale}) => {
  // Validate that the incoming `locale` parameter is valid
  if (!locales.includes(locale as any)) {
    // Optionally redirect or fallback to default locale
    // For now, we'll assume valid locale is always passed
    // or handled by middleware
    console.error(`Invalid locale: ${locale}`);
    // Fallback to English messages
    locale = 'en';
  }
 
  return {
    messages: (await import(`../public/locales/${locale}/common.json`)).default
  };
});

