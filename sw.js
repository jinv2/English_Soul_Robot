const CACHE_NAME = 'soul-robot-v1';
const ASSETS = [
    './',
    './index.html',
    './Crayon.css',
    './soul_bridge.js',
    './worker.js',
    './agent_logic.js',
    './assets/ignite.mp3',
    './assets/thinking.mp3',
    './assets/success.mp3',
    'https://cdn.jsdelivr.net/npm/@xenova/transformers@3.5.0',
    'https://fonts.googleapis.com/css2?family=Indie+Flower&family=Permanent+Marker&display=swap'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(ASSETS);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
