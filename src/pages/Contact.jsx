// src/pages/Contact.jsx
import Layout from "../components/Layout";

export default function Contact() {
  return (
    <Layout>
      <h2 className="text-3xl font-bold text-blue-700 mb-4">Contact Us</h2>
      <p className="text-gray-700">
        For queries about ScrapeMate or collaborations, reach out at: 
        <span className="font-semibold"> support@scrapemate.com </span>
      </p>
    </Layout>
  );
}