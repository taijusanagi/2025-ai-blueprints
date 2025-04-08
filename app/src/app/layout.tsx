import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "TrustML – Verifiable Federated Learning",
  description: "TrustML enables decentralized, verifiable training using Filecoin, smart contracts, and Merkle proofs.",
  openGraph: {
    title: "TrustML – Verifiable Federated Learning",
    description: "Train ML models across multiple nodes with trust. Powered by Filecoin.",
    images: [
      {
        url: "/ogp.png", // Make sure this file exists in your public/ directory
        width: 1200,
        height: 630,
        alt: "TrustML Landing Page",
      },
    ],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "TrustML – Verifiable Federated Learning",
    description: "Train ML models across multiple nodes with trust. Powered by Filecoin.",
    images: ["/ogp.png"],
  },
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
