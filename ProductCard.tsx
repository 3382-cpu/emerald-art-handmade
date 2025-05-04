// src/components/ProductCard.tsx
"use client";

import React from "react";
import Link from "next/link";
import { useTranslations, useLocale } from "next-intl"; // Import useLocale

// Define the structure of a product object
interface Product {
  id: number;
  name: string; // Name should come translated from API
  description: string; // Description should come translated from API
  price_usd: number;
  image_urls: string; // JSON string like ["url1", "url2"]
  available_colors: string; // JSON string like ["red", "blue"]
}

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const t = useTranslations("ProductsPage"); // Use translations from ProductsPage section
  const locale = useLocale(); // Get current locale

  let imageUrl = "/placeholder-image.jpg"; // Default placeholder
  try {
    const urls = JSON.parse(product.image_urls);
    if (Array.isArray(urls) && urls.length > 0) {
      imageUrl = urls[0]; // Use the first image
    }
  } catch (e) {
    console.error("Failed to parse image_urls:", product.image_urls);
  }

  let colors: string[] = [];
  try {
    const parsedColors = JSON.parse(product.available_colors || "[]");
    if (Array.isArray(parsedColors)) {
      colors = parsedColors;
    }
  } catch (e) {
    console.error("Failed to parse available_colors:", product.available_colors);
  }

  return (
    <div className="bg-card p-4 rounded-lg shadow-md border border-border flex flex-col h-full">
      {/* Link uses locale automatically via middleware */}
      <Link href={`/products/${product.id}`} className="block mb-4">
        <img
          src={imageUrl}
          alt={product.name} // Alt text should ideally be translated if possible
          className="w-full h-48 object-cover rounded-md transition-transform duration-300 hover:scale-105"
        />
      </Link>
      <div className="flex-grow">
        <h3 className="text-xl font-semibold mb-2 text-foreground">
          <Link href={`/products/${product.id}`} className="hover:text-primary">
            {product.name} {/* Name comes from API, assumed translated */}
          </Link>
        </h3>
        <p className="text-muted-foreground mb-3 text-sm line-clamp-3">
          {product.description} {/* Description comes from API, assumed translated */}
        </p>
        {/* Optional: Display colors */}
        {colors.length > 0 && (
          <div className="mb-3 text-xs text-muted-foreground">
            {/* TODO: Translate "Colors:" if needed */}
            Colors: {colors.join(", ")}
          </div>
        )}
      </div>
      <div className="mt-auto flex justify-between items-center pt-3 border-t border-border/50">
        <span className="text-lg font-bold text-primary">
          ${product.price_usd.toFixed(2)}
        </span>
        {/* Add to Cart button - functionality to be added later */}
        <button className="bg-primary text-primary-foreground px-4 py-1.5 rounded-md text-sm font-semibold hover:bg-primary/90 transition-colors">
          {t("addToCart")} {/* Use translation */}
        </button>
      </div>
    </div>
  );
};

export default ProductCard;

