class Client {
    // == Navigation ==
    static go_to_overview() {
        window.location.href = "/";
    }

    static go_to_login() {
        window.location.href = "/login";
    }

    static go_to_new_campaign(name) {
        window.location.href = "/new_campaign/" + String(name);
    }

    static go_to_campaign(name) {
        window.location.href = "/campaign/" + String(name);
    }

    // == Components ==
    static campaign_list(success, failure) {
        const token = sessionStorage.getItem("token");
        $.ajax({
            url: "/components/campaigns",
            type: "GET",
            headers: {
                Authorization: "Bearer " + token,
            },
            success: success,
            error: failure,
        });
    }

    // == Campaign ==
    static create_campaign(name, inputs, outputs, success, failure) {
        const token = sessionStorage.getItem("token");
        $.ajax({
            url: "/create_campaign/" + String(name),
            type: "POST",
            headers: {
                Authorization: "Bearer " + token,
            },
            contentType: "application/json",
            data: JSON.stringify({
                inputs: inputs,
                outputs: outputs,
            }),
            success: success,
            error: failure,
        });
    }

    static load_campaign(name, success, failure) {
        const token = sessionStorage.getItem("token");
        $.ajax({
            url: "/campaign_data/" + String(name),
            type: "GET",
            headers: {
                Authorization: "Bearer " + token,
            },
            contentType: "application/json",
            success: success,
            error: failure,
        });
    }
}
