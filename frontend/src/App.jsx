import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

const API_URL = "http://localhost:8000/chat";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = [
      [],
      {
        coder: {
          messages: [{ content: input, type: "human", name: "coder" }],
        },
      },
    ];

    const flatMessages = flattenMessages([...messages, userMessage]);

    setMessages([...messages, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: flatMessages }),
      });

      const data = await res.json();

      if (Array.isArray(data)) {
        setMessages((prev) => [...prev, ...data]);
      } else {
        console.error("Unexpected response format:", data);
      }
    } catch (err) {
      console.error("API error:", err);
    } finally {
      setLoading(false);
    }
  };

  const flattenMessages = (groupedMessages) => {
    const flat = [];

    for (const [, content] of groupedMessages) {
      if (content.agent?.messages) {
        for (const msg of content.agent.messages) {
          flat.push({ ...msg, type: "ai" });
        }
      }
      if (content.tools?.messages) {
        for (const msg of content.tools.messages) {
          flat.push({ ...msg, type: "tool" });
        }
      }
      if (content.coder?.messages) {
        for (const msg of content.coder.messages) {
          flat.push({ ...msg, type: "human", name: "coder" });
        }
      }
      if (content.supervisor) {
        flat.push({
          type: "system",
          content: `supervisor step: ${JSON.stringify(content.supervisor)}`,
        });
      }
    }

    return flat;
  };

  const handleEnter = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const renderMarkdown = (text) => (
    <ReactMarkdown
      children={text}
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
            <code className="bg-gray-200 px-1 rounded" {...props}>
              {children}
            </code>
          );
        },
      }}
    />
  );

  return (
    <div className="min-h-screen bg-gray-100 p-4 flex flex-col items-center">
      <div className="w-full max-w-xl bg-white rounded-2xl shadow-md p-6 flex flex-col gap-4">
        <h2 className="text-xl font-bold text-center">LangChain Chat</h2>
        <div className="flex flex-col gap-2 max-h-[400px] overflow-y-auto">
          {messages.map(([, content], idx) => {
            const role = content.coder
              ? "user"
              : content.agent
              ? "assistant"
              : content.tools
              ? "tool"
              : "system";

            const msgBlock =
              content.coder?.messages ||
              content.agent?.messages ||
              content.tools?.messages ||
              [];

            return msgBlock.map((msg, subIdx) => (
                <div
                  key={`${idx}-${subIdx}`}
                  className={`p-3 rounded-lg ${
                    role === "user"
                      ? "bg-blue-100 self-end"
                      : "bg-gray-200 self-start"
                  }`}
                >
                <div className="prose max-w-none">
                  {typeof msg.content === "string"
                    ? renderMarkdown(msg.content)
                    : msg.content.map((c, i) =>
                        c.text
                          ? renderMarkdown(c.text)
                          : c.input?.code
                          ? renderMarkdown("```python\n" + c.input.code + "\n```")
                          : null
                      )}
                </div>
              </div>
            ));
          })}
        </div>

        <textarea
          rows={2}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleEnter}
          placeholder="Type a message and hit Enter..."
          className="w-full p-2 rounded border resize-none"
        />

        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Thinking..." : "Send"}
        </button>
      </div>
    </div>
  );
}

export default App;
