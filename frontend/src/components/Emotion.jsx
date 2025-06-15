import { useState } from "react";
import axios from "axios";

import Highlighter from "react-highlight-words";

function Emotion() {
    const [input, setInput] = useState("");
    const [result, setResult] = useState(null);
    const [expl, setExpl] = useState(null);
    const [words1, setWords1] = useState(null);
    const [words2, setWords2] = useState(null);
    const colours = ["#FF9078" , "#EBFF78" , "#99FF78" , "#78FFE2" , "#78B5FF" , "#BE78FF" ]
    const handleSubmit = async () => {
        try {
            const res = await axios.get("http://localhost:8000/");
            setResult(res.data);
            // setInput(res.data.text)
            const topEmotion = Object.entries(res.data.predictions)
                .sort((a, b) => b[1] - a[1])[0][0];
            
            const threshold = 0.1;
            const filtered = {};
            for (const [emotion, wordPairs] of Object.entries(res.data.explanations)) {
                if(emotion===topEmotion)
                    filtered[emotion] = wordPairs.filter(([word, score]) => (score >= threshold));
            }

            const topEmotion2 = Object.entries(res.data.predictions)
                .sort((a, b) => b[1] - a[1])[1][0];
            console.log(topEmotion2)
            const filtered2 = {};

            for (const [emotion, wordPairs] of Object.entries(res.data.explanations)) {
                if(emotion===topEmotion2)
                    filtered2[emotion] = wordPairs.filter(([word, score]) => (score >= threshold));
            }
            const mergedFiltered = { ...filtered, ...filtered2 };

            const words1 = Object.values(filtered).flat().map(([word]) => word);
            const words2 = Object.values(filtered2).flat().map(([word]) => word);
            setWords1(words1);
            setWords2(words2);

            console.log(words1);
            console.log(mergedFiltered);
            setExpl(filtered);
        }
        catch(err) {
            console.error(err);
            alert("api fail");
        }
    }

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
                            <th>Key Words</th>
                        </tr>
                        {Object.entries(result.predictions).map(([emotion, val], idx) => (
                            <tr key={idx}>
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
