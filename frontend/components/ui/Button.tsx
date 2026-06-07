import React, { ReactNode } from "react";

interface BtnProps extends React.ComponentProps<"button"> {
    children: ReactNode,
    variant: 'primary' | 'secondary' | 'icon',
    className: string
}

interface StyleVariants {
    primary: string,
    secondary: string,
    icon: string
}

const base = "w-full py-4 rounded-2xl font-semibold active:scale-[0.98] transition-all flex items-center justify-center gap-2";

const variants: StyleVariants = {
    primary: `bg-primary text-white hover:bg-primary-hover shadow-lg shadow-primary-shadow`,
    secondary: `bg-secondary text-slate-700 hover:bg-secondary-hover`,
    icon: `w-20 h-20 rounded-full shadow-xl transition-all duration-300`
}

const Button = ({children, variant, className, ...props}: BtnProps) => {
  return <button {...props} className={`${base} ${variants[variant]} ${className}`} >{children}</button>;
};

export default Button;
