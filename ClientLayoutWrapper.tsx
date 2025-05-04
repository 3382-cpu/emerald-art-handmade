// src/components/ClientLayoutWrapper.tsx
"use client";

import React from "react";
import { NextIntlClientProvider, useMessages } from "next-intl";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export default function ClientLayoutWrapper({ 
  children,
  locale
}: {
  children: React.ReactNode;
  locale: string;
}) {
  // Receive messages provided in `i18n.ts` - This hook requires "use client"
  const messages = useMessages();

  return (
    <NextIntlClientProvider locale={locale} messages={messages}>
      <Header />
      <main className="flex-grow container mx-auto px-4 py-8">
        {children}
      </main>
      <Footer />
    </NextIntlClientProvider>
  );
}

