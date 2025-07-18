addEventListener('fetch', event => {
    event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Handle API endpoint for listing recaps
    if (path === '/api/recaps') {
        try {
            // In a real Cloudflare Worker, we would use the KV store or R2
            // For now, we'll return a list of all .txt files
            const response = await fetch('https://api.github.com/repos/yourusername/yourrepo/contents/');
            const files = await response.json();
            const recaps = files
                .filter(file => file.name.endsWith('_recap.txt'))
                .map(file => file.name);
            
            return new Response(JSON.stringify(recaps), {
                headers: { 'Content-Type': 'application/json' }
            });
        } catch (error) {
            return new Response(JSON.stringify({ error: 'Failed to fetch recaps' }), {
                status: 500,
                headers: { 'Content-Type': 'application/json' }
            });
        }
    }

    // Handle individual recap files
    if (path.startsWith('/recap/')) {
        const fileName = path.split('/').pop();
        if (fileName.endsWith('_recap.txt')) {
            try {
                // In a real Cloudflare Worker, we would fetch the file from KV or R2
                const response = await fetch(`https://raw.githubusercontent.com/yourusername/yourrepo/main/${fileName}`);
                const text = await response.text();
                
                // Create a simple HTML page to display the recap
                const html = `
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Game Recap: ${fileName.replace('_recap.txt', '')}</title>
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <style>
                            body { 
                                font-family: Arial, sans-serif; 
                                line-height: 1.6; 
                                max-width: 800px; 
                                margin: 0 auto; 
                                padding: 20px;
                            }
                            pre { 
                                white-space: pre-wrap; 
                                background: #f5f5f5; 
                                padding: 15px; 
                                border-radius: 5px;
                                overflow-x: auto;
                            }
                            .back-link { 
                                display: inline-block; 
                                margin-bottom: 20px; 
                                color: #3498db; 
                                text-decoration: none;
                            }
                            .back-link:hover { text-decoration: underline; }
                        </style>
                    </head>
                    <body>
                        <a href="/" class="back-link">← Back to all recaps</a>
                        <h1>${fileName.replace('_recap.txt', '').replace(/_/g, ' ')}</h1>
                        <pre>${text}</pre>
                    </body>
                    </html>
                `;
                
                return new Response(html, {
                    headers: { 'Content-Type': 'text/html' }
                });
            } catch (error) {
                return new Response('Recap not found', { status: 404 });
            }
        }
    }

    // For all other requests, serve the static files
    return fetch(request);
}
