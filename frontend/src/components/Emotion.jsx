import { useState } from "react";
import axios from "axios";

import Highlighter from "react-highlight-words";
import "./Emotion.css"

//  add spinning loader 


import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine
} from "recharts";

// const data = [
//   {
//     name: "disgust",
//     thats: 4000,
//     ugly: 2400,
//     amt: 2400
//   },
  
// ];


    


function Emotion() {
    const [input, setInput] = useState("");
    const [result, setResult] = useState(null);
    const [expl, setExpl] = useState(null);
    const [words1, setWords1] = useState(null);
    const [words2, setWords2] = useState(null);
    const colours = ["#FF9078" , "#EBFF78" , "#99FF78" , "#78FFE2" , "#78B5FF" , "#BE78FF" ]

    const colours_text = Array.from({ length: 500 }, () =>
        `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`
        );

    // console.log(colours_text)

    
          


    const handleSubmit = async (modelType) => {
        try {
            const res = await axios.post("http://localhost:8000/", { text: input, model_type: modelType });
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
            .filter(([word, score]) => (score) >= explanationThreshold)
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
                            <th>Graph</th>
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
                                
                                <td>
                                    {
                Object.entries(result.explanations).map(([emotion2, val], id) => {
                    const dataPoint = { name: emotion2 };
                      const sortedVal = [...val].sort((a, b) => b[1] - a[1]);

                        sortedVal.forEach(([word, weight]) => {
                        dataPoint[word] = weight;
                        });

                        const data = [dataPoint];

                        
                            console.log(data)
                    return(
                        <>
                        {emotion2===emotion && (
                    <BarChart
                      layout="vertical"
                        width={500}
                        height={200}
                        data={data}
                        // margin={{
                        //     top: 5,
                        //     right: 30,
                        //     left: 20,
                        //     bottom: 5
                        // }}
                            margin={{ top: 20, right: 1, left: 1, bottom: 5 }}

                        >

                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" />
                        <YAxis dataKey="word" type="category" />
                        <Tooltip />
                        <Legend />
                        <ReferenceLine y={0} stroke="#000" />
            
                            {sortedVal.map(([word], i) => (
                        <Bar key={i} dataKey={word} fill={colours_text[i % colours_text.length]} />                         
                        ))}

                    </BarChart>
                   )
                   }
               </> 
               
                )
                }
                )


            }
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
