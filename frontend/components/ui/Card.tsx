import React, { ComponentProps } from "react";



const Card = ({children, onClick, className = " "}: ComponentProps<"div">) => {
  return <div onClick={onClick}
            className={`p-5 border border-border rounded-2xl bg-surface shadow-sm hover:border-primary transition-all cursor-pointer flex items-center justify-between group ${className}`}>
            {children}
        </div>;
};

export default Card;
