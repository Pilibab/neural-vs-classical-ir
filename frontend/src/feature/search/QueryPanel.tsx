import CustomButton from "../../ui/CustomButton/CustomButton"
import CustomTextArea from "../../ui/CustomTextArea/CustomTextArea"
import "./QueryPanel.css"
import { getSimilarManhwa } from "../../service/mahwaService"
import { useContext, useState } from "react"
import ResultContext from "../../context/ResultContext"

const QueryPanel = () => {
    const [text, setText] = useState<string>("");

    const context = useContext(ResultContext);

    // If context is null, don't try to render or access properties
    if (!context) {
        throw new Error("QueryPanel must be used within a ResultProvider");
    }

    const { setResults } = context;


    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        // pass to service 
        console.log(`submitted: ${text}`)
        
        try {
            const response = await getSimilarManhwa(text);
            const results = response.data
            // Use response.data because that's where the list lives
            if (response.status === "success") {
                setResults(response.data); 
                console.log("Manhwas found: ", response.data.length);
            } else {
                console.error("Search failed:", response.error);
            }

            setResults(results)

        } catch (err) {
            console.error("Network error:", err);
        }

    }

    return (
        <>
            <form 
                onSubmit={handleSubmit}
            >
                <CustomTextArea
                    // label="true"
                    placeholder="Enter synopsis"
                    rows={5}    // what is this 
                    onChange={(e: any) => setText(e.target.value)}
                />

                <CustomButton
                    type="submit"
                >
                    Search
                </CustomButton>
            </form>


        </>
    )
}

export default QueryPanel;