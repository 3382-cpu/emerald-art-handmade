// src/app/page.tsx
"use client"; // Required for using hooks like useTranslations

import React from "react";
import ProductCard from "@/components/ProductCard";
import { useTranslations } from "next-intl";

// Placeholder for fetching featured products - replace with API call later
// TODO: Fetch products based on locale from API
const featuredProducts = [
  {
    id: 1,
    name: "Elegant Pink Bouquet", // Name should come translated from API ideally
    description: "A beautiful arrangement of artificial pink roses and lilies.", // Description should come translated
    price_usd: 45.99,
    image_urls: JSON.stringify(["/7a0aff92d03451c81611aaef3064a980.jpg"]), 
    available_colors: JSON.stringify(["Pink", "White"]),
  },
  {
    id: 2,
    name: "Luxury Mirror Decor",
    description: "Stunning mirror adorned with handcrafted flowers.",
    price_usd: 79.99,
    image_urls: JSON.stringify(["/f8c78a78a60958e26f178756084dff01.jpg"]), 
    available_colors: JSON.stringify(["Gold", "Silver"]),
  },
  {
    id: 3,
    name: "Classic White Bouquet",
    description: "Timeless beauty with artificial white orchids and greenery.",
    price_usd: 55.00,
    image_urls: JSON.stringify(["/6e42512ae6b2b33be21607dfe1f8703f.jpg"]), 
    available_colors: JSON.stringify(["White"]),
  },
];

export default function HomePage() {
  const t = useTranslations("HomePage");

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-16 bg-gradient-to-r from-secondary via-white to-secondary rounded-lg shadow">
        <h1 className="text-4xl font-bold mb-4 text-primary">{t("welcome")}</h1>
        <p className="text-xl text-foreground/80 mb-8">{t("tagline")}</p>
        <a
          href="/products" // Link to products page
          className="inline-block bg-primary text-primary-foreground px-8 py-3 rounded-md font-semibold hover:bg-primary/90 transition-colors"
        >
          {t("shopNow")}
        </a>
      </section>

      {/* Featured Products Section */}
      <section>
        <h2 className="text-3xl font-semibold mb-8 text-center text-primary">{t("featuredProducts")}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {featuredProducts.map((product) => (
            // Pass product data to ProductCard
            // Note: Product name/description ideally come translated from the API
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </section>

    </div>
  );
}

