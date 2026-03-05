const WB_Receiver = {
    async sendToEngine(endpoint, formData, isJson = false) {
        const options = {
            method: isJson ? 'DELETE' : 'POST',
            body: isJson ? JSON.stringify(formData) : formData
        };
        if (isJson) options.headers = { 'Content-Type': 'application/json' };

        const response = await fetch(`http://localhost:8080/api/v1/${endpoint}`, options);
        return response.json();
    }
};
