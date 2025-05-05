// src/App.jsx
import { useState } from 'react';

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hi, I’m VERA. What brings you here today?' }
  ]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: 'user', content: input }];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/onboard/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ conversation: newMessages })
      });

      const data = await res.json();
      if (data.response) {
        setMessages([...newMessages, { role: 'assistant', content: data.response }]);
      } else {
        setMessages([...newMessages, { role: 'assistant', content: 'Hmm... I didn’t quite catch that.' }]);
      }
    } catch (err) {
      console.error(err);
      setMessages([...newMessages, { role: 'assistant', content: 'Oops! Something went wrong.' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '600px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '1.5rem', marginBottom: '1rem' }}>VERA Onboarding</h1>
      <div style={{ border: '1px solid #ccc', padding: '1rem', marginBottom: '1rem', height: '300px', overflowY: 'auto', borderRadius: '6px' }}>
        {messages.map((m, i) => (
          <p key={i}><strong>{m.role === 'assistant' ? 'VERA' : 'You'}:</strong> {m.content}</p>
        ))}
        {loading && <p><em>VERA is thinking...</em></p>}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
        placeholder="Type your message here..."
        style={{ width: '80%', padding: '0.5rem' }}
      />
      <button onClick={sendMessage} style={{ padding: '0.5rem', marginLeft: '0.5rem' }}>Send</button>
    </div>
  );
}

export default App;
