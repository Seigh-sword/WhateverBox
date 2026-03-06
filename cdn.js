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

const WhateverBox = {
    project: "",
    token: "",

    init(p, t) {
        this.project = p;
        this.token = t;
    },

    async get(target, mode = 'gv') {
        const params = new URLSearchParams({
            project: this.project,
            token: this.token,
            mode: mode,
            target: target
        });

        if (mode === 'file') {
            const response = await fetch(`https://whateverbox.onrender.com/api/v1/get?${params}`);
            return await response.blob();
        }

        return WB_Receiver.sendToEngine(`get?${params}`, null, false);
    },

    async put(name, value, mode = 'gv') {
        const data = new FormData();
        data.append("project", this.project);
        data.append("token", this.token);
        data.append("mode", mode);
        
        if (mode === 'gv') {
            data.append("name", name);
            data.append("value", value);
        } else {
            data.append("file", value);
        }
        
        return WB_Receiver.sendToEngine('put', data);
    }
};
