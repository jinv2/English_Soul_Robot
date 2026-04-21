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
        this.isIgnited = false;
    }

    async ignite() {
        if (this.isIgnited) return;
        
        console.log("🔥 Igniting Soul Engine (Pure JS Brain)...");
        
        if (this.config.useWebGPU) {
            this.worker = new Worker(new URL('./worker.js', import.meta.url), { type: 'module' });
            
            return new Promise((resolve, reject) => {
                this.worker.onmessage = (e) => {
                    if (e.data.status === 'ready') {
                        this.isIgnited = true;
                        resolve(true);
                    } else if (e.data.status === 'error') {
                        reject(new Error(e.data.msg));
                    }
                };
                // Use the new protocol
                this.worker.postMessage({ type: 'init' });
            });
        }
        
        this.isIgnited = true;
        return true;
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
