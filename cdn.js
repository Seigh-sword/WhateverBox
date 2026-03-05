const WhateverBox = {
    project: "",
    token: "",

    init(projectName, userToken) {
        this.project = projectName;
        this.token = userToken;
    },

    async uploadFile(file) {
        const data = new FormData();
        data.append("project", this.project);
        data.append("token", this.token);
        data.append("mode", "file");
        data.append("file", file);
        return WB_Receiver.sendToEngine('push', data);
    },

    async saveVar(name, value) {
        const data = new FormData();
        data.append("project", this.project);
        data.append("token", this.token);
        data.append("mode", "var");
        data.append("name", name);
        data.append("value", value);
        return WB_Receiver.sendToEngine('push', data);
    },

    async nuke() {
        return WB_Receiver.sendToEngine('nuke', {
            project: this.project,
            token: this.token
        }, true);
    }
};
