import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ART-T Security Toolkit",
  description: "Advanced AI Red Teaming & Policy Validation Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}