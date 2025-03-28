import Link from "next/link";
import './globals.css';
export const metadata = {
  title: "Music Generation",
  description: "A simple Next.js app",
};

export default function Layout({ children }) {
  return (
    <html lang="en">
      <body className="bg-gray-100 text-gray-900">
        <nav className="bg-gradient-to-r from-slate-900 to-slate-700 text-white p-4 shadow-md flex  gap-6">
          <Link href="/" className="hover:underline font-bold">Home</Link>
          {/* <Link href="/upload" className="hover:underline font-bold">Upload files</Link> */}
          <Link href="/user" className="hover:underline font-bold">Upload via User</Link>
        </nav>
        <main className="p-6">{children}</main>
      </body>
    </html>
  );
}
