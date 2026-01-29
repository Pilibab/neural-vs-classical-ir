import { useContext } from "react";
import ResultContext from "../../../context/ResultContext";
import DisplayInfoCard from "../DisplayInfo/DisplayInfoCard";
import "./ManhwaCard.css";

interface ManhwaCardProps {
    idx: number
}

const ManhwaCard = ({ idx }: ManhwaCardProps) => {
    const context = useContext(ResultContext);

    if (!context) {
        throw new Error("ManhwaCard must be used within a ResultProvider");
    }

    const { resultsVectorSearch } = context;

    // console.log(resultsVectorSearch?.[idx]);
    

    // Optional: Add a safety check to avoid "cannot read property of undefined"
    const item = resultsVectorSearch?.[idx];

    if (!item) {
        return (
            <div className="manhwa-card">
                <p>Loading or No Data...</p>
            </div>
        );
    }
    console.log(item.cover_image_url);
    
    return (
        <div className="manhwa-card">
            <div className="image-container">
                <img src={item.cover_image_url} alt={`${item.title}.png cover `} />
                <DisplayInfoCard idx={idx} />
            </div>
            <p>{item.title}</p>
        </div>
    );
};

export default ManhwaCard;