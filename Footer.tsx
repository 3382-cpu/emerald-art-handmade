// src/components/Footer.tsx
"use client";

import React from "react";
import { useTranslations } from "next-intl";

const Footer: React.FC = () => {
  const t = useTranslations("Footer");
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-secondary text-secondary-foreground mt-12 py-6 shadow-inner">
      <div className="container mx-auto px-4 text-center">
        <p className="text-sm mb-2">{t("description")}</p>
        <p className="text-xs text-muted-foreground">
          {t("copyright", { year: currentYear })}
        </p>
        {/* Add other footer links if needed (e.g., Privacy Policy, Terms) */}
      </div>
    </footer>
  );
};

export default Footer;

