import { useState } from "react";
import axios from "axios";

import Highlighter from "react-highlight-words";
import "./Emotion.css"

function Emotion() {
    const [input, setInput] = useState("");
    const [result, setResult] = useState(null);
    const [expl, setExpl] = useState(null);
    const [words1, setWords1] = useState(null);
    const [words2, setWords2] = useState(null);
    const colours = ["#FF9078" , "#EBFF78" , "#99FF78" , "#78FFE2" , "#78B5FF" , "#BE78FF" ]

    const handleSubmit = async (modelType) => {
        try {
            const res = await axios.post("http://localhost:8000/a", { text: input, model_type: modelType });
            setResult(res.data);
        }
        catch(err) {
            console.error(err);
            alert("api fail");
        }
    }

    // const handleSubmit2 = async () => {
    //     try {
    //         const res = await axios.get("http://localhost:8000/a");
    //         setResult(res.data);
    //         // setInput(res.data.text)
      
    //     }
    //     catch(err) {
    //         console.error(err);
    //         alert("api fail");
    //     }
    // }

    function getImportantWords(data, predictionWord, explanationThreshold, predictionThreshold) {
        const predictionScore = data.predictions[predictionWord];
        if (predictionScore === undefined || predictionScore < predictionThreshold) {
            return [];
        }

        const explanationPairs = data.explanations[predictionWord];
        if (!explanationPairs) {
            return [];
        }

        return explanationPairs
            .filter(([word, score]) => Math.abs(score) >= explanationThreshold)
            .map(([word]) => word);
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

            <div className="models">
                <button onClick={() => handleSubmit("1")} className="buttonsubmit">
                    Analyze 1
                </button>

                <button onClick={() => handleSubmit("2")} className="buttonsubmit">
                    Analyze 2
                </button>

                <button onClick={() => handleSubmit("3")} className="buttonsubmit">
                    Analyze 3
                </button>

                <button onClick={() => handleSubmit("4")} className="buttonsubmit">
                    Analyze 4
                </button>
            </div>
            {result && (
                <div className="result-div"> 
                    <h3>Predicted Emotions</h3>
                    <table className="table">
                        <tr className="tableTop">
                            <th>Emotion</th>
                            <th>Value</th>
                            <th>Key Words</th>
                        </tr>
                        {Object.entries(result.predictions).map(([emotion, val], idx) => (
                            <tr key={idx} className="tableBottom">
                                <td>{emotion}</td>
                                <td>{val}</td>
                                <td>
                                    <Highlighter
                                        highlightClassName="highlight"
                                        searchWords={getImportantWords(result, emotion, 0.1 , 0.3)}
                                        autoEscape={true}
                                        textToHighlight={result.text}
                                        highlightStyle={{ backgroundColor: colours[idx] }}
                                    />
                                </td>
                            </tr>
                        ))}
                    </table>
                </div>
            )}
        </div>
    );
}

export default Emotion;
