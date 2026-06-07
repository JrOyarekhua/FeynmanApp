import React from "react";
import { LayoutDashboard } from "lucide-react"
const Header = () => {
  return (
    <header className="flex items-center justify-between py-6 w-full max-w-2xl mx-auto px-6">
      <div className="flex items-center gap-3">
        <div
          className={`w-10 h-10 bg-primary rounded-xl flex items-center justify-center shadow-lg shadow-primary-shadow`}
        >
           {/* logo goes here */}
          <LayoutDashboard className="w-6 h-6 text-white" />
        </div>
        <h1
          className={`text-2xl font-bold text-text-main tracking-tight`}
        >
          {/* name goes here */}
          EvaLogic
        </h1>
      </div>
      <div
        className={`w-10 h-10 rounded-full bg-secondary border-2 border-border`}
      />
    </header>
  );
};

export default Header;
