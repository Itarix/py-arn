$("#buttonComparePosition").click(function (event) {
    event.preventDefault(); /* prevent form submiting here */
    const button = (this)

    const arn1Value = $("#inputArn1").val();
    const arn2Value = $("#inputArn2").val();

    const messageButton = $("#messageButton");
    messageButton.text("");
    if (arn1Value === "" || arn2Value === "") {
        messageButton.text("Arn1 or Arn2 are empty");
        return
    }

    button.disabled = true;

    $.ajax({
        type: "POST",
        url: "http://127.0.0.1:5000/compare/position",
        data: {
            "arn1": arn1Value,
            "arn2": arn2Value,
        },
        dataType: "json",
        success: function (data) {
            $("#textSequenceArn1").text(data["arn1"]);
            $("#textSequenceArn2").text(data["arn2"]);

            $("#textSizeArn1").text(data["size_arn1"]);
            $("#textSizeArn2").text(data["size_arn2"]);

            $("#textNbMismatch").text(data["nb_mismatch"]);

            const htmlArnRed = `
                    <span class="text-danger">%s</span>
            `;
            const htmlArnGreen = `
                    <span class="text-success">%s</span>
            `;
            let textDiffArn1 = $("#textDiffArn1")
            for (let i = 0; i < data["arn1"].length; i++) {
                if (i >= data["arn2"].length) {
                    textDiffArn1.append(htmlArnRed.replace("%s", data["arn1"][i]));
                    continue;
                }
                if (data["arn1"][i] === data["arn2"][i]) {
                    textDiffArn1.append(htmlArnGreen.replace("%s", data["arn1"][i]));
                } else {
                    textDiffArn1.append(htmlArnRed.replace("%s", data["arn1"][i]));
                }
            }

            let textDiffArn2 = $("#textDiffArn2")
            for (let i = 0; i < data["arn2"].length; i++) {
                if (i >= data["arn1"].length) {
                    textDiffArn2.append(htmlArnRed.replace("%s", data["arn2"][i]));
                    continue;
                }
                if (data["arn1"][i] === data["arn2"][i]) {
                    textDiffArn2.append(htmlArnGreen.replace("%s", data["arn2"][i]));
                } else {
                    textDiffArn2.append(htmlArnRed.replace("%s", data["arn2"][i]));
                }
            }

            const htmlToAddInfosComparison = `
                <div class="tmp row">
                    <div class="col border border-secondary text-center">
                        <p>%s</p>
                    </div>
                </div>
            `;

            const divInfosBadSize = $("#divInfosBadSize");
            for (let i = 0; i < data["bad_sizes"].length; i++) {
                divInfosBadSize.append(htmlToAddInfosComparison.replace("%s", data["bad_sizes"][i]));
            }

            const divInfosBadValue = $("#divInfosBadValue");
            for (let i = 0; i < data["bad_values"].length; i++) {
                divInfosBadValue.append(htmlToAddInfosComparison.replace("%s", data["bad_values"][i]));
            }

            const divToast = $("#liveToast");
            const toast = new bootstrap.Toast(divToast);
            toast.show();

            button.disabled = false;
        },
        error: function (data) {
            button.disabled = false;
            messageButton.text(data.stringify());
        },
    });
});

$("#buttonClear").click(function (event) {
    event.preventDefault(); /* prevent form submiting here */
    const button = (this)
    button.disabled = true;

    $("#inputArn1").val("");
    $("#inputArn2").val("");
    $("#messageButton").text("");

    $("#textSizeArn1").text("");
    $("#textSizeArn2").text("");
    $("#textSequenceArn1").text("");
    $("#textSequenceArn2").text("");

    $("#textNbMismatch").text("");

    $("#textDiffArn1").text("");
    $("#textDiffArn2").text("");

    $(".tmp").remove();

    button.disabled = false;
});