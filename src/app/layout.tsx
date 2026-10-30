import type { Metadata } from "next";
import "./globals.css";
import { siteConfig } from "@/content/site";

export const metadata: Metadata = {
  title: `${siteConfig.name} — Video Editor`,
  description:
    "Professional video editor specializing in YouTube editing, short-form content, cinematic storytelling, and retention-focused cuts. Portfolio of Krishna Mishra / EditForge.",
  keywords: [
    "Video Editor",
    "YouTube Editing",
    "Short-Form Editing",
    "Video Editing Portfolio",
    "Cinematic Editing",
    "Krishna Mishra",
    "EditForge",
  ],
  authors: [{ name: siteConfig.name }],
  icons: {
    icon: "/icon.svg",
  },
  openGraph: {
    title: `${siteConfig.name} — Video Editor`,
    description:
      "Video editing that makes good content hit harder. YouTube, Shorts, cinematic edits.",
    type: "website",
    images: [{ url: siteConfig.banner }],
  },
  twitter: {
    card: "summary_large_image",
    title: `${siteConfig.name} — Video Editor`,
    description: "Video editing that makes good content hit harder.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
