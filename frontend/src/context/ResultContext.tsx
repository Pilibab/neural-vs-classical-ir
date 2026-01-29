import { createContext } from "react";
import type { VectorSearchMeta } from "../domain/manhwa/VectorSearchMeta";

export interface ResultContextValue {
    resultsVectorSearch: VectorSearchMeta[];
    setResultsVectorSearch: React.Dispatch<React.SetStateAction<VectorSearchMeta[]>>;

    clearResults: () => void;
}

const ResultContext = createContext<ResultContextValue | null>(null);

export default ResultContext;
