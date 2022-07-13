const staticPyPWA = "dev-pypwa-v4"
const assets = [
    // "",
    // "/",
    "/static/css/site.css",
    "/static/js/site.js",
    "/static/js/pwa-scaffold.js",

    "/static/python/frontend/client.py",
    "/static/python/frontend/weather_api.py",
    "/static/python/frontend/weather_report.py",

    "/static/pyscript/pyscript.css",
    "/static/pyscript/pyscript.js",
    "/static/pyscript/pyscript.py",

    "/static/images/weather/cloudy.png",
    "/static/images/weather/rain.png",
    "/static/images/weather/offline.png",
    "/static/images/weather/sunny.png",

    "/static/pyodide/pyodide.js",
    "/static/pyodide/packages.json",
    "/static/pyodide/pyodide_py.tar",
    "/static/pyodide/pyodide.asm.js",
    "/static/pyodide/pyodide.asm.data",
    "/static/pyodide/pyodide.asm.wasm",
    "/static/pyodide/micropip-0.1-py3-none-any.whl",
    "/static/pyodide/pyparsing-3.0.7-py3-none-any.whl",
    "/static/pyodide/packaging-21.3-py3-none-any.whl",
    "/static/pyodide/distutils.tar",

    "/static/images/icons/icon-144x144.png",
]

self.addEventListener("install", installEvent => {
    installEvent.waitUntil(
        caches.open(staticPyPWA).then(cache => {
            cache.addAll(assets).then(r => {
                console.log("Cache assets downloaded");
            }).catch(err => console.log("Error caching item", err))
            console.log(`Cache ${staticPyPWA} opened.`);
        }).catch(err => console.log("Error opening cache", err))
    )
})

self.addEventListener("fetch", fetchEvent => {
    fetchEvent.respondWith(
        caches.match(fetchEvent.request).then(res => {
            return res || fetch(fetchEvent.request)
        }).catch(err => console.log("Cache fetch error: ", err))
    )
})