import ResultContext from "../context/ResultContext"
import {useState, type PropsWithChildren } from "react";
import type { VectorSearchMeta } from "../feature/search/types";

type ResultProviderProps = PropsWithChildren<{}>;

const ResultProvider = ({children} : ResultProviderProps) => {
    const [results, setResults] = useState<VectorSearchMeta[]>([]);

    const clearResults = () => setResults([]);

    return (<ResultContext.Provider 
        value={{
        results, setResults, clearResults
        }}
    >
        {children}
    </ResultContext.Provider>)
}

export default ResultProvider;