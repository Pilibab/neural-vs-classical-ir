import type {ResultsPanelProps}  from "./types";
import "./ResultPanel.css";



const ResultsPanel = ({ currIdx, resultsVectorSearch }: ResultsPanelProps) => {
    if (resultsVectorSearch.length === 0) {
        return <p>No results found.</p>;
    }

    return (
        <div className="results-panel">
        </div>
    );
};

export default ResultsPanel;
