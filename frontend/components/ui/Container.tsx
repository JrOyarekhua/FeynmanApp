import React, { ReactNode } from "react";

interface Props {
    children: ReactNode
}

const Container = ({ children }: Props) => {
  return <section className="`w-full max-w-2xl h-[90vh] md:h-[800px] bg-surface shadow-2xl rounded-[2rem] p-6 sm:p-8 overflow-hidden flex flex-col ring-1 ring-border`">{children}</section>;
};

export default Container;
