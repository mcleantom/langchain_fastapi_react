import { 
  Routes,
  BrowserRouter,
  Route
} from "react-router-dom";
import Chat from "./Chat";

const API_URL = "http://localhost:8000/chat";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/chat/:chatId" element={<Chat />} />
        <Route path="*" element={<div>404 Not Found</div>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App;
