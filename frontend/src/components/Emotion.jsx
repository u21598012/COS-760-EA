import { useState } from "react";
import axios from "axios";

import Highlighter from "react-highlight-words";
import "./Emotion.css"
import { useEffect } from "react";
//  add spinning loader 


/*
]


*/

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

function Emotion() {
    const [input, setInput] = useState("");
    const [result, setResult] = useState(null);
    const [modelNo, setModelNo] = useState("");
    const [loading, setLoading] = useState(false);

    const colours = ["#FF9078" , "#EBFF78" , "#99FF78" , "#78FFE2" , "#78B5FF" , "#BE78FF" ]

    const storedColours = localStorage.getItem("colours_text");
    const parsedColours = JSON.parse(storedColours);

    // console.log(colours_text)
          
    //  add spinning loader  AND MAKE TEXT THE TEXT

    const handleSubmit = async (modelType) => {
        try {
            if(input===""){
                alert("Textfield cant be empty")
                return;
            }
            setLoading(true);
            const res = await axios.post("http://localhost:8000/", { text: input, 
                model_type: modelType , lime_iterations:1000 , decision_boundary : 0.5});
            setResult(res.data);
            console.log(res.data);
            setModelNo(modelType);
            setLoading(false);
        }
        catch(err) {
            console.error(err);
            alert("API Fail");
            setModelNo("");
            setLoading(false);
        }
        finally{
            setLoading(false);
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

    function getImportantWords(data, predictionWord, explanationThreshold, predictionBoolean) {
        const predictionScore = data.probabilities[predictionWord];
        if (predictionScore === undefined || !predictionBoolean) {
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
                    Fine-tuned mBERT  
                </button>

                <button onClick={() => handleSubmit("2")} className="buttonsubmit">
                    Zero-Shot XLM  
                </button>

                <button onClick={() => handleSubmit("3")} className="buttonsubmit">
                    Fine-tuned XLM  
                </button>

                <button onClick={() => handleSubmit("4")} className="buttonsubmit">
                    Zero-Shot BERT  
                </button>
            </div>
            {loading && <div className="spinner">Loading...</div>}
            {result && !loading && (
                <div className="result-div"> 
                    <h3>Predicted Emotions {modelNo ? "(model " + modelNo +")" : ""}</h3>
                    <table className="table">
                        <tr className="tableTop">
                            <th>Emotion</th>
                            <th>Value</th>
                            <th>Emotion Detected</th>

                            <th>Key Words</th>
                            <th>Graph</th>
                        </tr>
                        {Object.entries(result.probabilities).map(([emotion, val], idx) => (
                            <tr key={idx} className="tableBottom">
                                <td>{emotion}</td>
                                <td>{val}</td>
                                <td>{String(result.predictions[emotion])}</td>

                                <td>
                                    <Highlighter
                                        highlightClassName="highlight"
                                        searchWords={getImportantWords(result, emotion, 0.001 , result.predictions[emotion])}
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

                        
                            // console.log(data)
                    return(
                        <>
                        {emotion2===emotion && (
                    <BarChart
                      layout="vertical"
                        width={500}
                        height={200}
                        data={data}
                        margin={{ top: 20, right: 1, left: 1, bottom: 5 }}
                        >

                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis type="number" />
                        <YAxis dataKey="word" type="category" />
                        <Tooltip />
                        <Legend />
                        <ReferenceLine y={0} stroke="#000" />
            
                            {sortedVal.map(([word], i) => (
                        <Bar key={i} dataKey={word} fill={parsedColours[i % parsedColours.length]} />                         
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
