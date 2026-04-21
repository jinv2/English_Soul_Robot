/**
 * worker.js - Pure JavaScript Soul Core
 * Implementing shensist_brain.py logic directly in JS for 0-latency.
 */

import { pipeline, env } from 'https://cdn.jsdelivr.net/npm/@xenova/transformers@3.5.0';

// 强制压榨 WebGPU 性能配置
env.allowLocalModels = false; 
env.useBrowserCache = true;

let engine = {
    generator: null,
};

/**
 * 核心：模拟原 shensist_brain.py 的“灵魂提取”逻辑
 * 将单词转化为“机器人协议指令”
 */
const brainLogic = (text) => {
    const creativitySeed = Math.random();
    return `[Protocol_v3.5] Identity: Shensist-X. Exploration Word: ${text}. MISSION: Transform ${text} into a physical craft. Seed: ${creativitySeed.toFixed(2)}`;
};

self.onmessage = async (e) => {
    const { type, data } = e.data;

    if (type === 'init') {
        const modelName = 'Xenova/flan-t5-small'; // Nano-scale & functional
        
        try {
            // Priority 1: WebGPU
            if (!navigator.gpu) throw new Error("WebGPU not available in navigator");
            
            engine.generator = await pipeline('text2text-generation', modelName, {
                device: 'webgpu',
                dtype: 'q4',
            });
            self.postMessage({ status: 'ready', mode: 'webgpu', msg: '🚀 GPU Engine Roaring!' });
        } catch (error) {
            console.warn("WebGPU fallback to WASM:", error.message);
            try {
                // Priority 2: WASM
                engine.generator = await pipeline('text2text-generation', modelName, {
                    device: 'wasm',
                    dtype: 'q4',
                });
                self.postMessage({ status: 'ready', mode: 'wasm', msg: 'Robot thinking with WASM parts...' });
            } catch (wasmError) {
                self.postMessage({ status: 'error', mode: 'error', msg: 'Engine failure: ' + wasmError.message });
            }
        }
    }

    if (type === 'process') {
        try {
            const soulOutput = brainLogic(data);
            const result = await engine.generator(soulOutput, {
                max_new_tokens: 64,
                temperature: 0.8,
                do_sample: true
            });
            self.postMessage({ status: 'result', data: result[0].generated_text });
        } catch (error) {
            self.postMessage({ status: 'error', msg: "Processing error: " + error.message });
        }
    }
};
