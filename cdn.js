const WhateverBox = {
    project: "",
    token: "",

    init(projectName, userToken) {
        this.project = projectName;
        this.token = userToken;
    },

    async get(target, mode = 'gv') {
        const params = new URLSearchParams({
            project: this.project,
            token: this.token,
            mode: mode,
            target: target
        });
        
        const url = `https://whateverbox.onrender.com/api/v1/get?${params}`;
        
        if (mode === 'file') {
            let attempt = 1;
            while (attempt <= 5) {
                try {
                    const response = await fetch(url);
                    if (response.ok) return await response.blob();
                    throw new Error();
                } catch (e) {
                    if (attempt === 5) throw e;
                    await new Promise(r => setTimeout(r, attempt * 2000));
                    attempt++;
                }
            }
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
