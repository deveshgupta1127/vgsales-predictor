import { useState } from "react";
import axios from "axios";

export default function Predict() {
  const [formData, setFormData] = useState({
    Platform: "PS4",
    Genre: "Action",
    Publisher: "Activision",
    Critic_Score: 75,
    User_Score: 7.5,
  });
  const [prediction, setPrediction] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const res = await axios.post("http://localhost:5000/predict", formData);
    setPrediction(res.data.prediction);
  };

  return (
    <div className="container">
      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map((key) => (
          <div key={key}>
            <label>{key}</label>
            <input
              type="text"
              name={key}
              value={formData[key]}
              onChange={handleChange}
            />
          </div>
        ))}
        <button type="submit">Predict</button>
      </form>
      {prediction && <div><h3>Predicted Sales: {prediction}M</h3></div>}
    </div>
  );
}