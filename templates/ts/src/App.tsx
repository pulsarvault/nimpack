import React, { useState } from "react";

export default function App(): JSX.Element {
  const [count, setCount] = useState<number>(0);
  return (
    <div style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>Hello from Nimpack + React + TypeScript 🚀</h1>
      <p>Hot reload is working!</p>
      <button onClick={() => setCount(count + 1)}>
        Clicked {count} times
      </button>
    </div>
  );
}
