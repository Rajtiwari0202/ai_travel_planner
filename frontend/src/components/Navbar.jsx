import React from "react";

const Navbar = () => {
  return (
    <nav className="flex justify-between items-center py-5 px-8 bg-transparent">
      <h1 className="text-2xl font-bold text-white">TaskPilot</h1>
      <ul className="hidden md:flex space-x-8 text-gray-200">
        <li className="hover:text-white cursor-pointer">Home</li>
        <li className="hover:text-white cursor-pointer">Features</li>
        <li className="hover:text-white cursor-pointer">About</li>
        <li className="hover:text-white cursor-pointer">Login</li>
      </ul>
    </nav>
  );
};

export default Navbar;
