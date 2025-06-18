import "react"
import {useState, useEffect} from "react"

export function MCQChallenge({challenge, showExplanation = false}) {
    const [selectedOption, setSelectedOption] = useState(null)
    const [shouldShowExplanation, setShouldShowExplanation] = useState(showExplanation)

    // Reset selection when challenge changes
    useEffect(() => {
        setSelectedOption(null)
        setShouldShowExplanation(showExplanation)
    }, [challenge, showExplanation])

    const options = typeof challenge.options === "string"
        ? JSON.parse(challenge.options)
        : challenge.options

    const handleOptionSelect = (index) => {
        if (selectedOption !== null) return;
        setSelectedOption(index)
        setShouldShowExplanation(true)
    }

    const getOptionClass = (index) => {
        if (selectedOption === null) return "option"

        if (selectedOption === index) {
            return index === challenge.correct_answer_id 
                ? "option correct" 
                : "option incorrect"
        }
        
        if (selectedOption !== null && index === challenge.correct_answer_id) {
            return "option correct"
        }

        return "option"
    }

    return <div className="challenge-display">
        <div className="challenge-header">
            <span className="difficulty-badge">{challenge.difficulty}</span>
        </div>
        <div className="challenge-content">
            <h2 className="challenge-title">{challenge.title}</h2>
            <div className="options-container">
                {options.map((option, index) => (
                    <div
                        className={getOptionClass(index)}
                        key={index}
                        onClick={() => handleOptionSelect(index)}
                    >
                        <span className="option-marker">{String.fromCharCode(65 + index)}.</span>
                        <span className="option-text">{option}</span>
                    </div>
                ))}
            </div>
        </div>
        {shouldShowExplanation && selectedOption !== null && (
            <div className="explanation-container">
                <h3>Explanation</h3>
                <div className="explanation-content">
                    <p>{challenge.explanation}</p>
                    <div className="result-message">
                        {selectedOption === challenge.correct_answer_id 
                            ? "✅ Correct!" 
                            : "❌ Incorrect. The correct answer is highlighted in green."}
                    </div>
                </div>
            </div>
        )}
    </div>
}