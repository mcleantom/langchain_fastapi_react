import { useEffect, useState } from "react";
import {
  useParams
} from "react-router-dom";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";


const Chat = () => {
  const { chatId } = useParams();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (chatId) {
      fetch(`http://localhost:8000/chat/${chatId}`)
        .then((res) => res.json())
        .then((data) => setMessages(data.channel_values.messages))
        .catch((err) => console.error("Error fetching chat: ", err));
    }
  }, [chatId]);

  const renderMessage = (msg, index) => {
    const isUser = msg.type === "human";

    return (
      <div
        key={msg.id || index}
        className={`flex ${isUser ? "justify-end" : "justify-start"}`}
      >
        <div
          className={`max-w-xs md:max-w-md px-4 py-2 rounded-2xl text-sm ${
            isUser
              ? "bg-blue-600 text-white rounded-br-sm"
              : "bg-gray-200 text-black rounded-bl-sm"
          }`}
        >
          <ReactMarkdown
            children={msg.content}
            components={{
              code({ node, inline, className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || "");
                return !inline && match ? (
                  <SyntaxHighlighter
                    style={oneDark}
                    language={match[1]}
                    PreTag="div"
                    {...props}
                  >
                    {String(children).replace(/\n$/, "")}
                  </SyntaxHighlighter>
                ) : (
                  <code className="bg-gray-100 px-1 rounded" {...props}>
                    {children}
                  </code>
                );
              },
            }}
          />
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-grey-100 p-4 flex flex-col items-center">
      <div className="w-full max-w-xl bg-white rounded-2xl shadow-md p-6 flex flex-col gap-4">
        <h2 className="text-xl font-bold text-center">LangChain Chat</h2>
        <div className="flex flex-col gap-2 max-h-[400px] overflow-y-auto">
          {messages.map((msg, index) => renderMessage(msg, index))}
        </div>

        <textarea
          rows={2}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message and hit Enter..."
          className="w-full p-2 rounded border resize-none"
        />

        <button
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>
    </div>
  );
};


export default Chat;