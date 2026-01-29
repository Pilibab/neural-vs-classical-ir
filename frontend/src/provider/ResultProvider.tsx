import ResultContext from "../context/ResultContext"
import {useState, type PropsWithChildren } from "react";
import type { VectorSearchMeta } from "../domain/manhwa/VectorSearchMeta";

type ResultProviderProps = PropsWithChildren<{}>;

const ResultProvider = ({children} : ResultProviderProps) => {
    const [resultsVectorSearch, setResultsVectorSearch] = useState<VectorSearchMeta[]>([]);

    const clearResults = () => {
        setResultsVectorSearch([])
    };

    return (<ResultContext.Provider 
        value={{
        resultsVectorSearch, setResultsVectorSearch, clearResults
        }}
    >
        {children}
    </ResultContext.Provider>)
}

export default ResultProvider;