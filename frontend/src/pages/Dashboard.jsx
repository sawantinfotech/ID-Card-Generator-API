import { useState } from "react";
import { generateID } from "../api";

export default function Dashboard() {
  const user = JSON.parse(localStorage.getItem("user"));
  const [name, setName] = useState("");
  const [format, setFormat] = useState("pdf");
  const [photo, setPhoto] = useState(null);
  const [result, setResult] = useState(null);

  const handleGenerate = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("name", name);
    formData.append("output_format", format);
    formData.append("photo", photo);
    formData.append("api_key", user.api_key);
    formData.append("api_secret", user.api_secret);

    try {
      const res = await generateID(formData);
      setResult(res.data.file_path);
    } catch {
      alert("Generation failed");
    }
  };

  return (
    <div className="container">
      <h2>Welcome, {user?.username}</h2>
      <p>Your API Key: <b>{user.api_key}</b></p>
      <p>Your API Secret: <b>{user.api_secret}</b></p>

      <form onSubmit={handleGenerate}>
        <input value={name} placeholder="Name on ID" onChange={(e) => setName(e.target.value)} required /><br />
        <select value={format} onChange={(e) => setFormat(e.target.value)}>
          <option value="pdf">PDF</option>
          <option value="image">Image</option>
        </select><br />
        <input type="file" accept="image/*" onChange={(e) => setPhoto(e.target.files[0])} required /><br />
        <button type="submit">Generate ID Card</button>
      </form>

      {result && (
        <div>
          <p>✅ Generated: <a href={`/${result}`} target="_blank" rel="noopener noreferrer">{result}</a></p>
        </div>
      )}
    </div>
  );
}
