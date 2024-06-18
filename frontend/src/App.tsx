import { GoogleOAuthProvider } from "@react-oauth/google";
import axios from "axios";
import { useCallback, useState } from "react";
import GoogleLogin from "./components/GoogleLogin";

const CLIENT_ID = import.meta.env.VITE_CLIENT_ID;

function App() {
  const [accessToken, setAccessToken] = useState("");
  const [data, setData] = useState<{
    search_data: string[];
    youtube_data: string[];
  }>();

  const setToken = (token: string) => {
    setAccessToken(token);
  };

  const handleButtonClick = useCallback(() => {
    axios
      .post("http://127.0.0.1:5000/api/collect-data", { accessToken })
      .then((response) => {
        console.log(response.data);
        if (response.data) {
          setData(response.data);
        }
      })
      .catch((err) => console.error("Error collecting data:", err));
  }, [accessToken]);

  return (
    <GoogleOAuthProvider clientId={CLIENT_ID}>
      <GoogleLogin setToken={setToken} />
      <button onClick={handleButtonClick} disabled={!accessToken}>
        구글 검색기록 수집
      </button>

      <br />
      <br />
      <br />

      <div>
        <span>검색 기록</span>
        <ul>
          {data?.search_data.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>
      <div>
        <span>시청 기록</span>
        <ul>
          {data?.youtube_data.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </div>
    </GoogleOAuthProvider>
  );
}

export default App;
