// src/components/Navbar.jsx
import { useState } from "react";
import { Link } from "react-router-dom";

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-blue-600 text-white px-1 py-1 flex justify-between items-center">
      {/* Logo */}
      <Link to="/" className="flex items-center">
        <img
          src="/logo.png"
          alt="ScrapeMate Logo"
          className="h-30 w-30"
        />
        {/* <span className="text-xl font-bold">ScrapeMate</span> */}
      </Link>

      {/* Desktop Menu */}
      <div className="hidden md:flex space-x-6">
        <Link to="/" className="text-xl font-bold hover:text-yellow-300 p-4">Home</Link>
        <Link to="/about" className="text-xl font-bold hover:text-yellow-300 p-4">About</Link>
        <Link to="/contact" className="text-xl font-bold hover:text-yellow-300 mr-10 p-4">Contact</Link>
      </div>

      {/* Hamburger Button */}
      <button
        className="md:hidden focus:outline-none"
        onClick={() => setIsOpen(!isOpen)}
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
            d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="absolute top-16 left-0 w-full bg-blue-700 flex flex-col items-center space-y-4 py-4 md:hidden">
          <a href="/" className="hover:text-yellow-300">Home</a>
          <a href="/about" className="hover:text-yellow-300">About</a>
          <a href="/contact" className="hover:text-yellow-300">Contact</a>
        </div>
      )}
    </nav>
  );
}