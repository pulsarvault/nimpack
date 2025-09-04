import React, { useState } from "react";

export default function App(): JSX.Element {
    const [count, setCount] = useState(0);
    return (
        <main className="min-h-screen bg-slate-950 text-slate-100 flex items-center justify-center">
            <div className="p-8 rounded-2xl bg-slate-900 shadow">
                <h1 className="text-2xl font-bold mb-3">PyPack + React (TS) + Tailwind</h1>
                <p className="mb-4 opacity-80">Hello from React TS 🧪</p>
                <button
                    className="px-4 py-2 rounded bg-indigo-500 hover:bg-indigo-600 active:scale-95 transition"
                    onClick={() => setCount((c) => c + 1)}
                >
                    Count: {count}
                </button>
            </div>
        </main>
    );
}
