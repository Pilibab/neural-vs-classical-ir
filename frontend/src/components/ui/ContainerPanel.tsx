import "./ContainerPanel.css"
import React from "react";

interface ComponentProps {
    children: React.ReactNode;
}

const ContainerPanel = ({children}: ComponentProps) => {
    return (
        <div className="Container">
            {children}
        </div>
    )
}

export default ContainerPanel;