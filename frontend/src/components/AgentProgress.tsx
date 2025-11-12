// src/components/AgentProgress.tsx
import React from "react";
import { motion } from "framer-motion";
import type { Variants } from "framer-motion";


const list: Variants = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.12 } },
};

const item: Variants = {
  hidden: { opacity: 0, y: 6 },
  show: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 300, damping: 22 } },
};

export default function AgentProgress({ steps }: { steps: string[] }) {
  return (
    <div className="mt-4">
      <h3 className="font-medium">Agent Progress</h3>
      <motion.ul className="mt-2 space-y-1" initial="hidden" animate="show" variants={list}>
        {steps.map((s, i) => (
          <motion.li
            key={i}
            className="text-sm text-slate-200/90 flex items-center gap-2"
            variants={item}
          >
            <span className="w-2 h-2 rounded-full bg-linear-to-br from-indigo-400 to-blue-400 inline-block" />
            <span>{s}</span>
          </motion.li>
        ))}
      </motion.ul>
    </div>
  );
}
