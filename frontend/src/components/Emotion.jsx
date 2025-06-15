import { useState } from "react";
import axios from "axios";

function Emotion() {
    const [input, setInput] = useState("");
    const [result, setResult] = useState(null);
    const [expl, setExpl] = useState(null);

    const handleSubmit = async () => {
        try {
            const res = await axios.get("http://localhost:8000/");
            setResult(res.data);
            // setInput(res.data.text)
        }
        catch(err) {
            console.error(err);
            alert("api fail");
        }
    }

    return (
        <div className="outer">
            <h2 className="title">NLP Emotion Analyzer</h2>

            <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Enter text here"
                className="textarea"
            />
            <button onClick={handleSubmit} className="buttonsubmit">
                Analyze
            </button>

            {result && (
                <div className="result-div"> 
                    <h3>Predicted Emotions</h3>
                    <table className="table">
                        <tr>
                            <th>Emotion</th>
                            <th>Value</th>
                        </tr>
                        {Object.entries(result.predictions).map(([emotion, val], idx) => (
                            <tr key={idx}>
                                <td>{emotion}</td>
                                <td>{val}</td>
                            </tr>
                        ))}
                    </table>
                </div>
            )}
        </div>
    );
}

export default Emotion;
