import localFont from "next/font/local";
import "./globals.css";
import { Button } from "@/components/ui/button";
import { Moon, LogOut, Inbox } from "lucide-react";
import Link from "next/link";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
} from "@/components/ui/navigation-menu";
import { navigationMenuTriggerStyle } from "@/components/ui/navigation-menu";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="flex flex-col min-h-screen bg-background">
          <header className="flex items-center justify-between px-6 py-4 border-b">
            <div className="flex items-center space-x-4">
              <Link href="/" className="flex items-center space-x-2">
                <span className="text-2xl font-bold text-primary">
                  Supper CX
                </span>
              </Link>
              <nav className="hidden md:flex items-center space-x-4">
                <NavigationMenu>
                  <NavigationMenuList>
                    <NavigationMenuItem>
                      <Link href="/ticket" legacyBehavior passHref>
                        <NavigationMenuLink
                          className={navigationMenuTriggerStyle()}
                        >
                          <Inbox className="h-4 w-4 mr-2" />
                          Inbox
                        </NavigationMenuLink>
                      </Link>
                    </NavigationMenuItem>
                  </NavigationMenuList>
                </NavigationMenu>
              </nav>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-muted-foreground">
                1 / 100 drafts used
              </span>
              <Button variant="ghost" size="icon">
                <Moon className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon">
                <LogOut className="h-5 w-5" />
              </Button>
            </div>
          </header>
          <main className="flex-1 p-6">{children}</main>
        </div>
      </body>
    </html>
  );
}
