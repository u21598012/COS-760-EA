import { useState } from "react";
import axios from "axios";

function Emotion() {
    const [inputText, setInputText] = useState("");

    const handleSubmit = () => {
        alert("submitted")
    }

    return (
        <div className="outer">
        <h2 className="title">NLP Emotion Analyzer</h2>

        <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter text here"
            className="textarea"
        />
        <button onClick={handleSubmit} className="buttonsubmit">
            Analyze
        </button>

        </div>
    );
}

export default Emotion;
