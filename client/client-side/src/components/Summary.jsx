import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const medicalEntities = {
  diseases: ["diabetes", "cancer", "asthma", "hypertension", "stroke"],
  medications: ["aspirin", "metformin", "ibuprofen", "insulin", "paracetamol"],
  symptoms: ["fever", "cough", "fatigue", "headache", "dizziness"],
};

const fatalDiseases = ["cancer", "stroke", "hypertension"];

const highlightEntities = (text) => {
  if (!text) return "";

  Object.entries(medicalEntities).forEach(([category, words]) => {
    words.forEach((word) => {
      const regex = new RegExp(`\\b${word}\\b`, "gi");
      const color =
        category === "diseases"
          ? "text-red-600 font-bold"
          : category === "medications"
          ? "text-blue-600 font-bold"
          : "text-green-600 font-bold"; // Symptoms

      text = text.replace(
        regex,
        (match) => `<span class="${color}">${match}</span>`
      );
    });
  });

  return text.replace(/\n/g, "<br>");
};

const Summary = () => {
  const [summary, setSummary] = useState("");
  const [alertShown, setAlertShown] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("/summary.txt")
      .then((response) => response.text())
      .then((text) => {
        setSummary(text);
      })
      .catch((error) => console.error("Error loading summary:", error));
  }, []);

  useEffect(() => {
    if (!summary || alertShown) return;

    const hasFatalDisease = fatalDiseases.some((disease) =>
      summary.toLowerCase().includes(disease)
    );

    if (hasFatalDisease) {
      setAlertShown(true);
      const confirmNavigation = window.confirm(
        "A fatal disease has been detected. Do you want to search for nearby hospitals? OR Click 'Cancel' to continue reading the summary."
      );
      if (confirmNavigation) {
        navigate("/search");
      }

      // Reset the alertShown state after 1 minute (60000 milliseconds)
      const resetTimeout = setTimeout(() => {
        setAlertShown(false);
      }, 60000);

      // Cleanup the timeout if the component unmounts before the timeout completes
      return () => clearTimeout(resetTimeout);
    }
  }, [summary, alertShown, navigate]);

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">
        Medical Report Summary
      </h1>

      <div className="bg-gray-100 p-6 rounded-lg shadow-md overflow-x-auto max-w-full">
        <pre
          className="whitespace-pre-wrap break-words text-gray-700 text-lg md:text-xl leading-relaxed"
          dangerouslySetInnerHTML={{ __html: highlightEntities(summary) }}
        ></pre>
      </div>
    </div>
  );
};

export default Summary;
