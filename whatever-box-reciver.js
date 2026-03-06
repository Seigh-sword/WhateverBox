const WB_Receiver = {
    async sendToEngine(endpoint, formData, isJson = false, attempt = 1) {
        try {
            const options = {
                method: isJson ? 'DELETE' : 'POST',
                body: isJson ? JSON.stringify(formData) : formData
            };
            if (isJson) options.headers = { 'Content-Type': 'application/json' };

            const response = await fetch(`https://whateverbox.onrender.com/api/v1/${endpoint}`, options);
            
            if (!response.ok && response.status !== 404 && attempt <= 5) {
                throw new Error("Retryable error");
            }
            
            return await response.json();
        } catch (err) {
            if (attempt <= 5) {
                let delay = attempt * 2000;
                await new Promise(r => setTimeout(r, delay));
                return this.sendToEngine(endpoint, formData, isJson, attempt + 1);
            }
            throw err;
        }
    }
};
