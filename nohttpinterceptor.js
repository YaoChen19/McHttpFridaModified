Java.perform(function () {
    const showHeaders = true;

    const Request = Java.use("okhttp3.Request"); // okhttp3.Request
    

    const Response = Java.use("okhttp3.Response"); // okhttp3.Response
    
    const BridgeInterceptor = Java.use("okhttp3.internal.http.BridgeInterceptor"); // okhttp3.internal.http.BridgeInterceptor
    

    function formatHeaders(headers) {
        return headers.toString();
    }
    function interceptRequest(request) {
        let requestMethod = request.method();
        let requestUrl = request.url().toString();
        send(`[>] request intercepted: method=${requestMethod} url=${requestUrl}`);

        if (showHeaders) {
            send(" > headers:\n" + formatHeaders(request.headers()));
        }

        let requestBody = request.toString();
        send(" > body: " + requestBody);
        send("\n");
    }

    function interceptResponse(response) {
        send("[<] response intercepted: " + JSON.stringify(response.toString()));

        if (showHeaders) {
            send(" < headers:\n" + formatHeaders(response.headers()));
        }

        let responseBody = response.peekBody(1024 * 128); // okhttp3.Response::peekBody(byteCount: Long)
        if (responseBody != null) {
            let responseBodyString = responseBody.string();
            if (responseBodyString != "") {
                send(" < body: " + responseBodyString);
            }
        }
        send("\n");
    }

    BridgeInterceptor.intercept.implementation = function(chain) {
       
        let request = chain.request();
        interceptRequest(request);

        let response = this.intercept(chain);

        interceptResponse(response);
        return response;
    }
});