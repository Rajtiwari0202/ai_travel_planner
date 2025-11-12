// src/components/LoadingOverlay.tsx
import React from "react";
import { motion } from "framer-motion";
import type { Variants } from "framer-motion";


export default function LoadingOverlay({ visible }: { visible: boolean }) {
  const container: Variants = {
    hidden: { opacity: 0, pointerEvents: "none" },
    show: { opacity: 1, pointerEvents: "auto", transition: { staggerChildren: 0.08 } },
  };

  const plane: Variants = {
    hidden: { x: "-20%", opacity: 0, rotate: -10, scale: 0.9 },
    show: {
      x: "110%",
      opacity: 1,
      rotate: 0,
      scale: 1,
      transition: { duration: 2.2, ease: "easeInOut", repeat: Infinity, repeatType: "loop", repeatDelay: 0.6 },
    },
  };

  const pulse: Variants = {
    hidden: { scale: 0.95, opacity: 0.5 },
    show: { scale: 1.05, opacity: 1, transition: { yoyo: Infinity, duration: 0.9 } },
  };

  return (
    <motion.div
      initial="hidden"
      animate={visible ? "show" : "hidden"}
      variants={container}
      className="fixed inset-0 z-50 flex items-center justify-center"
    >
      {/* dimmed backdrop */}
      <div className={`absolute inset-0 bg-black/60 backdrop-blur-sm`} />

      {/* centered card */}
      <motion.div
        className="relative z-10 w-[80%] max-w-2xl p-6 rounded-2xl bg-gradient-to-br from-slate-800/80 to-slate-900/80 border border-white/6 shadow-2xl"
        initial={{ y: 20, opacity: 0 }}
        animate={visible ? { y: 0, opacity: 1 } : { y: 20, opacity: 0 }}
        transition={{ duration: 0.25 }}
      >
        <div className="flex items-center gap-4">
          {/* plane animation */}
          <div className="relative h-16 flex-1 overflow-hidden">
            <motion.div
              className="absolute top-1/2 -translate-y-1/2 text-4xl"
              variants={plane}
              aria-hidden
            >
              ✈️
              {/* optional add small cloud dots */}
            </motion.div>
          </div>

          <div className="flex-1">
            <motion.h3 className="text-lg font-semibold" variants={pulse}>
              Planning your trip…
            </motion.h3>
            <p className="text-sm text-slate-300 mt-1">
              Our agents are researching options and optimizing your itinerary — this usually takes a few seconds.
            </p>
          </div>

          <div className="w-24">
            <motion.div
              className="h-3 w-full rounded-full bg-white/8 overflow-hidden"
              variants={pulse}
            >
              <motion.div
                className="h-full bg-gradient-to-r from-blue-500 to-indigo-500"
                style={{ width: "40%" }}
                animate={{ x: [0, 120, 0] }}
                transition={{ duration: 1.1, repeat: Infinity, ease: "easeInOut" }}
              />
            </motion.div>
          </div>
        </div>

        <div className="mt-4 text-xs text-slate-400">
          <em>Tip:</em> you can interact with the UI while the agents run, and stop/restart at any time.
        </div>
      </motion.div>
    </motion.div>
  );
}
