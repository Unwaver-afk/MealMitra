const BASE_URL = import.meta.env?.VITE_API_URL || "/api";
const CONNECT_TIMEOUT_MS = 15_000;

/**
 * Simulated streaming chat client for MealMitra.
 * Connects to Django REST endpoint and renders a realistic smooth typing effect
 * on the frontend without requiring backend SSE infrastructure or external AI APIs.
 *
 * @param {object} params
 * @param {string} params.message
 * @param {{role:string,text:string}[]} params.history
 * @param {string} params.summary
 * @param {string} params.userContext
 * @param {AbortSignal} params.signal
 * @param {(delta: string) => void} params.onChunk
 * @param {(final: {text: string, summary: string}) => void} params.onDone
 * @param {(message: string) => void} params.onError
 */
export async function streamChat({ message, history, summary, userContext, signal, onChunk, onDone, onError }) {
    const controller = new AbortController();
    const abortFromCaller = () => controller.abort();
    signal?.addEventListener("abort", abortFromCaller, { once: true });

    let connectTimedOut = false;
    const connectTimeout = setTimeout(() => {
        connectTimedOut = true;
        controller.abort();
    }, CONNECT_TIMEOUT_MS);

    let data;
    try {
        const token = localStorage.getItem("token");
        const response = await fetch(`${BASE_URL}/chatbot/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                ...(token ? { Authorization: `Bearer ${token}` } : {}),
            },
            body: JSON.stringify({ message, history, summary, userContext }),
            signal: controller.signal,
        });

        if (!response.ok) {
            let msg = "The assistant is unavailable right now.";
            try {
                const errData = await response.json();
                if (errData?.message || errData?.error) msg = errData.message || errData.error;
            } catch {
                /* default */
            }
            onError(msg);
            signal?.removeEventListener("abort", abortFromCaller);
            return;
        }

        data = await response.json();
    } catch (err) {
        signal?.removeEventListener("abort", abortFromCaller);
        if (signal?.aborted) return;
        if (connectTimedOut) {
            onError("The assistant server took too long to respond. Please try again.");
            return;
        }
        if (err.name === "AbortError") return;
        onError("Couldn't reach the assistant. Check your connection and try again.");
        return;
    } finally {
        clearTimeout(connectTimeout);
    }

    const fullText = data.text || "";
    const responseSummary = data.summary || "MealMitra assistant discussed available meal subscriptions.";

    // Smooth frontend typing animation to simulate streaming effect
    // Splits text into words or characters and emits them with human-like cadence
    const words = fullText.split(/(\s+)/);
    let index = 0;

    const streamInterval = setInterval(() => {
        if (signal?.aborted) {
            clearInterval(streamInterval);
            signal?.removeEventListener("abort", abortFromCaller);
            return;
        }

        if (index < words.length) {
            const chunk = words[index];
            onChunk(chunk);
            index++;
        } else {
            clearInterval(streamInterval);
            signal?.removeEventListener("abort", abortFromCaller);
            onDone({ text: fullText, summary: responseSummary });
        }
    }, 28);
}
