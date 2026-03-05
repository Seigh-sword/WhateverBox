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
        const response = await fetch(`http://localhost:8080/api/v1/get?${params}`);
        if (mode === 'file') return response.blob();
        return response.json();
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
        
        const response = await fetch(`http://localhost:8080/api/v1/put`, {
            method: 'POST',
            body: data
        });
        return response.json();
    }
};
