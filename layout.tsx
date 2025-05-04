// src/app/layout.tsx
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
// Removed Header and Footer imports, they are now in ClientLayoutWrapper
// Removed NextIntlClientProvider and useMessages imports
import { notFound } from "next/navigation";
import ClientLayoutWrapper from "@/components/ClientLayoutWrapper"; // Import the new wrapper

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

import { locales } from "@/config/i18n.config"; // Import from central config

// Metadata can now be exported safely as this is a Server Component
export const metadata: Metadata = {
  title: "Emerald Art Handmade - Exquisite Handmade Bouquets",
  description: "Discover unique, handcrafted artificial flower bouquets and decor.",
};

export default function RootLayout({
  children,
  params: { locale },
}: Readonly<{
  children: React.ReactNode;
  params: { locale: string };
}>) {
  // Validate locale (remains server-side)
  if (!locales.includes(locale)) {
    notFound();
  }

  // useMessages hook is moved to ClientLayoutWrapper

  return (
    <html lang={locale} dir={locale === "ar" ? "rtl" : "ltr"}>
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased flex flex-col min-h-screen bg-background text-foreground`}
      >
        {/* Use the ClientLayoutWrapper for client-side parts */}
        <ClientLayoutWrapper locale={locale}>
          {children} {/* Pass children down */}
        </ClientLayoutWrapper>
      </body>
    </html>
  );
}

