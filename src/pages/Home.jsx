// src/pages/Home.jsx
import { useState } from "react";
import Layout from "../components/Layout";
import Landing from "./Landing"; // import the Landing component

export default function Home() {
  const [showLanding, setShowLanding] = useState(false);

  return (
    <Layout>
      {!showLanding ? (
        <div className="flex flex-col items-center justify-center min-h-[70vh] text-center">
          <h2 className="text-4xl font-bold text-blue-700 mb-6">
            Welcome to ScrapeMate
          </h2>
          <p className="text-gray-700 mb-8 max-w-xl">
            ScrapeMate helps you extract clean, line‑by‑line text data from any website.
            Perfect for building datasets for machine learning or research.
          </p>
          <button
            onClick={() => setShowLanding(true)}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
          >
            Let’s Get Started
          </button>
        </div>
      ) : (
        <Landing />
      )}
    </Layout>
  );
}