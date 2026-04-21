/**
 * SoulEngine - The core interaction bridge for the Shensist Matrix.
 * Manages WebGPU workers and the new Init/Process protocol.
 */
export class SoulEngine {
    constructor(config = {}) {
        this.config = {
            useWebGPU: true,
            precision: 'q4',
            style: 'crayon',
            ...config
        };
        this.worker = null;
        this.isIgnited = false; // Started loading
        this.isFullBrainReady = false; // Finished loading
    }

    /**
     * Silent Background Ignition
     * Starts the worker but does not return a blocking promise unless needed.
     */
    ignite() {
        if (this.isIgnited) return;
        this.isIgnited = true;
        
        console.log("🔥 Background Ignition: Soul Engine waking up...");
        
        try {
            this.worker = new Worker(new URL('./worker.js', import.meta.url), { type: 'module' });
            this.worker.onmessage = (e) => {
                if (e.data.status === 'ready') {
                    this.isFullBrainReady = true;
                    console.log("✅ Soul Engine: Full brain connected.");
                    // Dispatch a custom event for the UI to know it's ready
                    window.dispatchEvent(new CustomEvent('soul-ready', { detail: e.data }));
                } else if (e.data.status === 'error') {
                    console.error("❌ Soul Engine error:", e.data.msg);
                }
            };
            this.worker.postMessage({ type: 'init' });
        } catch (e) {
            console.error("❌ Failed to start worker:", e);
        }
    }

    async interact(word) {
        if (!this.isIgnited) await this.ignite();

        return new Promise((resolve, reject) => {
            const handler = (e) => {
                if (e.data.status === 'result') {
                    this.worker.removeEventListener('message', handler);
                    resolve({
                        spark: e.data.data,
                        memory: "In-browser memory core active.",
                        raw: e.data
                    });
                } else if (e.data.status === 'error') {
                    this.worker.removeEventListener('message', handler);
                    reject(new Error(e.data.msg));
                }
            };
            this.worker.addEventListener('message', handler);
            // Use the new protocol
            this.worker.postMessage({ type: 'process', data: word });
        });
    }
}
