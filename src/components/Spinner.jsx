// src/components/Spinner.jsx
import { motion } from "framer-motion";

export default function Spinner() {
  return (
    <motion.div
      className="h-12 w-12 border-4 border-gray-300 border-t-4 border-blue-600 rounded-full"
      animate={{ rotate: 360 }}
      transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
    />
  );
}