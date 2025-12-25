// src/components/Footer.jsx
export default function Footer() {
  return (
    <footer className="bg-blue-600 text-white py-4 text-center mt-10">
      <p>© {new Date().getFullYear()} ScrapeMate. All rights reserved.</p>
    </footer>
  );
}