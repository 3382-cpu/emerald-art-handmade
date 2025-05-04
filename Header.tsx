// src/components/Header.tsx
"use client"; // Mark as client component to use hooks

import React from "react";
import Link from "next/link";
import { useTranslations } from "next-intl";
import { usePathname } from "next/navigation";
import { locales } from "@/config/i18n.config"; // Import locales from central config

// Component for switching language
const LanguageSwitcher = () => {
  const t = useTranslations("Header");
  const pathname = usePathname();

  // Function to remove locale prefix from pathname
  const getPathWithoutLocale = (currentPath: string) => {
    for (const locale of locales) {
      if (currentPath.startsWith(`/${locale}`)) {
        return currentPath.substring(locale.length + 1) || "/"; // Remove /en or /ar
      }
    }
    return currentPath; // Return original path if no locale prefix found
  };

  const pathWithoutLocale = getPathWithoutLocale(pathname);

  return (
    <div className="flex space-x-2 text-sm">
      {locales.map((loc) => {
        const isActive = pathname.startsWith(`/${loc}`);
        return (
          <Link
            key={loc}
            href={`/${loc}${pathWithoutLocale}`}
            className={`px-2 py-1 rounded ${isActive ? "bg-primary text-primary-foreground font-semibold" : "text-muted-foreground hover:text-foreground"}`}
          >
            {loc === "ar" ? "العربية" : "English"}
          </Link>
        );
      })}
    </div>
  );
};

const Header: React.FC = () => {
  const t = useTranslations("Header");

  // Basic navigation links
  const navLinks = [
    { href: "/", labelKey: "home" },
    { href: "/products", labelKey: "products" },
    { href: "/about", labelKey: "about" },
    { href: "/contact", labelKey: "contact" },
    // TODO: Add conditional links for Login/Register/Profile based on auth state
    { href: "/login", labelKey: "login" },
    { href: "/register", labelKey: "register" },
    // { href: "/profile", labelKey: "profile" },
  ];

  return (
    <header className="bg-secondary shadow-md sticky top-0 z-50">
      <nav className="container mx-auto px-4 py-3 flex justify-between items-center">
        {/* Brand Name/Logo */}
        <Link href="/" className="text-2xl font-bold text-primary hover:text-primary/80">
          {t("brand")}
        </Link>

        {/* Navigation Links */}
        <ul className="hidden md:flex space-x-4 rtl:space-x-reverse">
          {navLinks.map((link) => (
            <li key={link.href}>
              <Link href={link.href} className="text-foreground hover:text-primary transition-colors">
                {t(link.labelKey)}
              </Link>
            </li>
          ))}
        </ul>

        {/* Language Switcher & Cart Icon */}
        <div className="flex items-center space-x-4">
          <LanguageSwitcher />
          {/* TODO: Add Cart Icon/Link here */}
          {/* TODO: Add Login/Account Icon/Link here (conditionally show Profile/Logout) */}
        </div>

        {/* TODO: Add Mobile Menu Button for smaller screens */}
      </nav>
    </header>
  );
};

export default Header;

