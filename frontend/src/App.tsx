import QueryPanel from "./feature/search/QueryPanel"
import ContainerPanel from "./ui/ContainerPanel/ContainerPanel"

import "./index.css"
import ResultsPanel from "./feature/search/ResultPanel"
import { useContext, useEffect, useState } from "react"
import CustomButton from "./ui/CustomButton/CustomButton"
import ResultContext from "./context/ResultContext"

function App() {

  const context = useContext(ResultContext);

  // If context is null, don't try to render or access properties
  if (!context) {
      throw new Error("QueryPanel must be used within a ResultProvider");
  }

  const { resultsVectorSearch} = context;

  useEffect(() => {

  }, [resultsVectorSearch]);


    const [currIdx, setCurrIdx] = useState(0)

    // helper ensures idx stays i bound 
    const canGoPrev = currIdx > 0;
    const canGoNext = currIdx < resultsVectorSearch.length - 1;

    const handleNext = () => {
        if (canGoNext) setCurrIdx(prevIdx => prevIdx + 1);
    };

    const handlePrev = () => {
        if (canGoPrev) setCurrIdx(prevIdx => prevIdx - 1);
    };

  return (
    <div className="App">
      <ContainerPanel>
        <QueryPanel/>

      </ContainerPanel>
      <ContainerPanel>
        <ResultsPanel currIdx={currIdx} resultsVectorSearch={resultsVectorSearch}/>
          {// TODO: MAKE IT SO THAT BUTTON IS NOT CLICKABLE FOR RESPECTIVE BOUND 
            }
          <div className="button-container">
            <CustomButton
                onClick={handlePrev} 
                disabled={!canGoPrev}
            >{"<"}</CustomButton>
            <CustomButton
                onClick={handleNext} 
                disabled={!canGoNext}
            >{">"}</CustomButton>            
          </div>
      </ContainerPanel>
    </div>
  )
}

export default App
