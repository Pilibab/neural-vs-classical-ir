import QueryPanel from "./components/panel/QueryPanel"
import ContainerPanel from "./components/ui/ContainerPanel"

import "./index.css"

function App() {

  return (
    <div className="App">
      <ContainerPanel>
        <QueryPanel/>
      </ContainerPanel>
      <ContainerPanel>
        {null}
      </ContainerPanel>
    </div>
  )
}

export default App
