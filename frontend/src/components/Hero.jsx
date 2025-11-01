import React from "react";
import { motion } from "framer-motion";

const Hero = () => {
  return (
    <section className="flex flex-col items-center justify-center text-center py-24 px-6 bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 min-h-screen">
      <motion.h1
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
        className="text-5xl md:text-6xl font-extrabold text-white mb-6"
      >
        AI-Powered Productivity for Teams 🚀
      </motion.h1>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 1 }}
        className="text-lg text-gray-200 max-w-2xl"
      >
        Streamline your workflow, automate repetitive tasks, and focus on what matters most — all with TaskPilot.
      </motion.p>

      <motion.button
        whileHover={{ scale: 1.05 }}
        className="mt-10 bg-white text-indigo-600 font-semibold py-3 px-8 rounded-2xl shadow-lg hover:bg-gray-100"
      >
        Get Started
      </motion.button>
    </section>
  );
};

export default Hero;
